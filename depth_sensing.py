########################################################################
#
# Copyright (c) 2017, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################
import math
import numpy as np
import pyzed.core as core
import pyzed.defines as sl


def func(tuple_arr, zed, unity):
    # Create and set PyRuntimeParameters after opening the camera
    point_cloud = core.PyMat()

    # A new image is available if grab() returns PySUCCESS
    unity.next_frame()
    # Retrieve colored point cloud. Point cloud is aligned on the left image.
    zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

    # Get and log distance value in mm at the center of the image
    # We measure the distance camera - object using Euclidean distance
    for tuple in range(len(tuple_arr)):
        x = tuple_arr[tuple][0]
        y = tuple_arr[tuple][1]
        err, point_cloud_value = point_cloud.get_value(x, y)
        distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                             point_cloud_value[1] * point_cloud_value[1] +
                             point_cloud_value[2] * point_cloud_value[2])

        if not np.isnan(distance) and not np.isinf(distance):
            # Unity calibration
            # 1280/720 = 25/x -> x = 14.0625
            # scaling factor will be 25/1280 and 14.0625/720 respectively
            # distance = (distance * float(25))/float(8000) # coz we want max range of 8m and unity has max scale of 100
            x = float(x * 25) / float(1280)
            y = float(y * 14.065) / float(720)
            # logging.debug("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
            unity.add((x, y, distance))
