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

py::tuple getCorners(Stag *stag) {
    py::tuple ret = py::tuple(stag->markers.size());
    for (int i=0; i<stag->markers.size(); i++) {
        std::vector<std::vector<double>> contours_vec;
        for (cv::Point2d pt : stag->markers[i].corners) {
            contours_vec.push_back({pt.x, pt.y});
        }
        py::array contours = py::cast(contours_vec);
        ret[i] = contours.reshape({1, 4, 2});
    }
    return ret;
}

py::array getIds(Stag *stag) {
    std::vector<int> ret_vec;
    for (const Marker& marker : stag->markers) {
        ret_vec.push_back(marker.id);
    }
    py::array ret = py::cast(ret_vec);
    return ret.reshape({-1, 1});
}

py::tuple getRejectedImgPoints(Stag *stag) {
    py::tuple ret = py::tuple(stag->falseCandidates.size());
    for (int i=0; i<stag->falseCandidates.size(); i++) {
        std::vector<std::vector<double>> contours_vec;
        for (cv::Point2d pt : stag->falseCandidates[i].corners) {
            contours_vec.push_back({pt.x, pt.y});
        }
        py::array contours = py::cast(contours_vec);
        ret[i] = contours.reshape({1, 4, 2});
    }
    return ret;
}

py::tuple detectMarkers(const Mat &inImage, int libraryHD, int errorCorrection=-1) {
    Stag stag(libraryHD, errorCorrection);
    stag.detectMarkers(inImage);
    py::tuple ret = py::make_tuple(getCorners(&stag), getIds(&stag), getRejectedImgPoints(&stag));
    return ret;
}

PYBIND11_MODULE(stag, m) {
    NDArrayConverter::init_numpy();
    m.def("detectMarkers", &detectMarkers, "Detect STag markers in image. Returns (corners, ids, rejectedImgPoints) of detected markers.");
}
