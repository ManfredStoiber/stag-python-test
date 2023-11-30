#include "submodules/pybind11_opencv_numpy/ndarray_converter.h"
#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include "submodules/stag/src/Marker.h"
#include "submodules/stag/src/Stag.h"
using cv::Mat;

namespace py = pybind11;
using namespace py::literals;


/**
 * Detects markers in given image.
 * @param inImage OpenCV Matrix of input image.
 * @param libraryHD The library HD that is used. Possible values are [11,&nbsp;13,&nbsp;15,&nbsp;17,&nbsp;19,&nbsp;21,&nbsp;23].
 * @param errorCorrection The amount of error correction that is going to be used.
 *  Value needs to be in range 0&nbsp;\<=&nbsp;errorCorrection&nbsp;\<=&nbsp;(HD-1)/2.\n
 *  If set to -1, the max possible value for the given library HD
 *  is used.
 * @returns Tuple of (corners, ids, rejectedImgPoints) of detected markers
 */
py::tuple detectMarkers(const Mat &inImage, int libraryHD, int errorCorrection=-1) {
    auto corners = std::vector<std::vector<cv::Point2f>>();
    auto ids = std::vector<int>();
    auto rejectedImgPoints = std::vector<std::vector<cv::Point2f>>();

    stag::detectMarkers(inImage, libraryHD, corners, ids, errorCorrection);
    py::tuple ret = py::make_tuple(corners, ids, rejectedImgPoints);
    return ret;
}

PYBIND11_MODULE(stag, m) {
    NDArrayConverter::init_numpy();
    m.def("detectMarkers", &detectMarkers, "Detect STag markers in given image.\n\t@param Test\n\t@Returns (corners, ids, rejectedImgPoints) of detected markers.");
}

int main() {
    cv::Mat image = cv::imread("example/example.jpg");
    return 0;
}
