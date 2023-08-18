from holoviews import opts
import cv2 as cv
import holoviews as hv
import holoviews.operation.datashader as ds
import numpy as np
import xarray as xr

from magnify.plot.ndplot import ndplot
import magnify.utils as utils


def roishow(assay: xr.Dataset, grid=None, slider=None, rasterize=False, **kwargs):
    if grid is None and slider is None:
        slider = ["channel", "time"]
        grid = ["mark"]

    def imfunc(assay: xr.Dataset, **kwargs):
        contours = get_contours(assay)
        plot = hv.Image((assay.roi_x, assay.roi_y, assay.roi)).opts(**kwargs)
        plot *= hv.Path(contours).opts(color="red")
        return plot

    plot = ndplot(assay, imfunc, grid=grid, slider=slider, **kwargs)
    plot = plot.opts(opts.Image(tools=["hover"]))
    return ds.rasterize(plot) if rasterize else plot


def imshow(
    assay: xr.Dataset,
    grid=None,
    slider=None,
    rasterize=False,
    compression_ratio=1,
    contour_type="roi",
    show_centers=False,
    label_offset=0.3,
    **kwargs,
):
    if grid is None and slider is None:
        slider = ["channel", "time"]

    def imfunc(assay: xr.Dataset, **kwargs):
        img = assay.image[..., ::compression_ratio, ::compression_ratio].compute()
        plot = hv.Image((img.im_x, img.im_y, img))
        if "roi" in assay:
            roi = assay.roi.compute()
            # Initialize image metadata.
            roi_len = roi.sizes["roi_y"] // compression_ratio
            contours = []
            labels = []
            for idx, m in roi.groupby("mark"):
                x = m.x.item() / compression_ratio
                y = m.y.item() / compression_ratio
                # Get the centers and the bounds of the bounding box.
                top, bottom, left, right = utils.bounding_box(
                    x, y, roi_len, img.sizes["im_x"], img.sizes["im_y"]
                )
                # Contours are either roi bounding boxes or contours around the foreground.
                if contour_type == "roi":
                    contours.append(hv.Bounds((left, bottom, right, top)))
                elif contour_type == "fg":
                    cont = get_contours(m)
                    # Adjust contours to be in image coordinates.
                    cont = [c + [left, top] for c in cont]
                    contours += cont

                # Get the label for the bounding box.
                if "tag" in m.coords:
                    label = f"{m.mark.item()}: {m.tag.item()}"
                else:
                    label = str(m.mark.item())
                labels.append((x, y - label_offset * roi_len, label))

            valid = assay.valid.to_numpy().flatten()
            # Overlay image, bounding boxes, and labels.
            plot *= hv.Path([b for b, v in zip(contours, valid) if v]).opts(color="green")
            plot *= hv.Path([b for b, v in zip(contours, valid) if not v]).opts(color="red")
            if show_centers:
                plot *= hv.Points((assay.x, assay.y)).opts(size=2, color="red")
            plot *= hv.Labels(labels)

        # Style the plot.
        plot = plot.opts(
            opts.Image(tools=["hover"]),
            opts.Labels(text_font_size="8pt", text_color="white"),
            opts.Path(line_width=1),
        )
        return plot

    img = ndplot(assay, imfunc, grid=grid, slider=slider, **kwargs)
    return ds.rasterize(img, line_width=1) if rasterize else img


def get_contours(roi):
    contours, _ = cv.findContours(
        roi.fg.to_numpy().astype("uint8"),
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE,
    )
    # Remove the extra dimension inserted by opencv.
    contours = [c[:, 0] for c in contours]
    # Close the curves.
    contours = [np.append(c, [c[0]], axis=0) for c in contours]
    return contours
