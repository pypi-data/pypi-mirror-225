# TODO: padding type

import numpy as np

from DeepStorm.Initializers.he import He
from DeepStorm.Initializers.constant import Constant
from DeepStorm.Layers.base import BaseLayer
from DeepStorm.logger import get_file_logger


_logger = get_file_logger(__name__, 'debug')


class Conv2d(BaseLayer):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, weights_initializer=He(), bias_initializer=Constant(0.1)):
        super().__init__()
        self.trainable = True
        self.initializable = True
        self._optimizer = None

        if isinstance(stride, int):
            stride = self.to_tuple(stride)
        self.stride_shape = stride
        self.stride_size_dim1 = self.stride_shape[0]
        self.stride_size_dim2 = self.stride_shape[1]

        self.in_channels = in_channels
        self.out_channels = out_channels

        if isinstance(kernel_size, int):
            kernel_size = self.to_tuple(kernel_size)
        self.kernel_size = kernel_size
        self.kernel_size_dim1 = self.kernel_size[0]
        self.kernel_size_dim2 = self.kernel_size[1]
        self.is_reduction_kernel = self.kernel_size == (1, 1)

        self.padding = padding

        self.weights_initializer = weights_initializer
        self.weight_shape = (
            self.out_channels, self.in_channels, *self.kernel_size)

        self.bias_initializer = bias_initializer

        self.initialize()

    def to_tuple(self, int_value):
        return (int_value, int_value)

    def check_padding_type(self, padding):
        if padding == "same":
            self.pad_size_dim1 = self.get_pad_size_same(self.kernel_size_dim1)
            self.pad_size_dim2 = self.get_pad_size_same(self.kernel_size_dim2)
        elif padding == "valid":
            self.pad_size_dim1 = (0, 0)
            self.pad_size_dim2 = (0, 0)
        elif isinstance(padding, int):
            self.pad_size_dim1 = (padding, padding)
            self.pad_size_dim2 = (padding, padding)

    def initialize(self):
        self.weights = self.weights_initializer.initialize(self.weight_shape, self.in_channels * self.kernel_size_dim1 * self.kernel_size_dim2,
                                                           self.kernel_size_dim1 * self.kernel_size_dim2 * self.out_channels)
        self.bias = self.bias_initializer.initialize(
            (self.out_channels, 1), self.out_channels, 1)

    @property
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, v):
        self._optimizer = v

    @property
    def gradient_weights(self):
        return self._gradient_weights

    @property
    def gradient_bias(self):
        return self._gradient_bias

    def get_shape_after_conv(self, dim_size, kernel_size, pad, stride) -> int:
        (start_pad, end_pad) = pad
        return 1 + (dim_size - kernel_size + start_pad + end_pad)//stride

    def get_pad_size_same(self, kernel_size):
        # if its an odd kernel
        if kernel_size % 2 == 1:
            start_pad = (kernel_size - 1)//2
            return (start_pad, start_pad)
        # else it is even
        start_pad = kernel_size//2 - 1
        end_pad = kernel_size//2
        return (start_pad, end_pad)

    def pad_img_same(self, imgs):
        (start_pad_dim1, end_pad_dim1) = self.pad_size_dim1
        (start_pad_dim2, end_pad_dim2) = self.pad_size_dim2
        return np.pad(imgs, ((0, 0), (0, 0), (start_pad_dim1, end_pad_dim1), (start_pad_dim2, end_pad_dim2)), mode="constant")

    def remove_pad(self, imgs):
        (start_pad_dim1, end_pad_dim1) = self.pad_size_dim1
        (start_pad_dim2, end_pad_dim2) = self.pad_size_dim2
        if self.is_reduction_kernel:
            return imgs
        return imgs[:, start_pad_dim1:-end_pad_dim1, start_pad_dim2:-end_pad_dim2]
    
    def pad_imgs(self, imgs):
        self.check_padding_type(self.padding)
        if self.padding == "same":
            return self.pad_img_same(imgs)

    def convolve(self, slice, kernel, bias):
        return np.sum(slice * kernel) + bias

    def get_output_shape_for_img(self, input_size_dim1, input_size_dim2):
        output_dim1 = self.get_shape_after_conv(
            input_size_dim1, self.kernel_size_dim1, self.pad_size_dim1, self.stride_size_dim1)
        output_dim2 = self.get_shape_after_conv(
            input_size_dim2, self.kernel_size_dim2, self.pad_size_dim2, self.stride_size_dim2)

        return (self.batch_size, self.out_channels, output_dim1, output_dim2)

    def generate_slice(self, image, output_dim1, output_dim2):
        for i in range(output_dim1):
            for j in range(output_dim2):
                start_dim1 = i * self.stride_size_dim1
                end_dim1 = start_dim1 + self.kernel_size_dim1
                start_dim2 = j * self.stride_size_dim2
                end_dim2 = start_dim2 + self.kernel_size_dim2
                slice = image[:, start_dim1:end_dim1, start_dim2:end_dim2]
                yield slice, i, j

    def forward(self, input_tensor: np.array):  # input shape BATCHxCHANNELSxHIGHTxWIDTH
        self.input_tensor = input_tensor
        (self.batch_size, _, input_size_dim1, input_size_dim2) = input_tensor.shape
        self.input_tensor_padded = self.pad_imgs(input_tensor)

        self.forward_output_shape = self.get_output_shape_for_img(
            input_size_dim1, input_size_dim2)
        (_, _, output_dim1, output_dim2) = self.forward_output_shape
        self.forward_output = np.zeros(self.forward_output_shape)

        for n in range(self.batch_size):
            one_sample_padded = self.input_tensor_padded[n]
            for out_channel in range(self.out_channels):
                kernel = self.weights[out_channel]
                bias = self.bias[out_channel]

                for slice, i, j in self.generate_slice(one_sample_padded, output_dim1, output_dim2):
                    self.forward_output[n, out_channel, i,
                                        j] = self.convolve(slice, kernel, bias)
        return self.forward_output

    def backward(self, error_tensor):
        (_, _, output_dim1, output_dim2) = self.forward_output_shape

        output = np.zeros_like(self.input_tensor)
        gradient_input = np.zeros_like(self.input_tensor_padded)
        self._gradient_bias = np.zeros((self.out_channels, 1, 1, 1))
        self._gradient_weights = np.zeros_like(self.weights)

        for n in range(self.batch_size):
            one_sample_padded = self.input_tensor_padded[n]

            for out_channel in range(self.out_channels):
                for slice, i, j in self.generate_slice(one_sample_padded, output_dim1, output_dim2):
                    start_dim1 = i * self.stride_size_dim1
                    end_dim1 = start_dim1 + self.kernel_size_dim1
                    start_dim2 = j * self.stride_size_dim2
                    end_dim2 = start_dim2 + self.kernel_size_dim2

                    self._gradient_weights[out_channel] += slice * \
                        error_tensor[n, out_channel, i, j]
                    self._gradient_bias[out_channel] += error_tensor[n,
                                                                     out_channel, i, j]
                    gradient_input[n, :, start_dim1:end_dim1, start_dim2:end_dim2] += error_tensor[n,
                                                                                                   out_channel, i, j] * self.weights[out_channel]

            output[n] = self.remove_pad(gradient_input[n])

        if self.optimizer:
            self.weights = self.optimizer.calculate_update(
                self.weights, self.gradient_weights)
            # Common mistake: pruning the bias usually harms model accuracy too much. (https://www.tensorflow.org/model_optimization/guide/pruning/comprehensive_guide#:~:text=Common%20mistake%3A%20pruning%20the%20bias%20usually%20harms%20model%20accuracy%20too%20much.)
        return output

