#!/bin/sh
#
# Copyright (c) 2022 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

IMAGE=$1
IMAGE_TAG=$2
export CONTAINER_TOOL=docker
export BASE_IMAGE="centos:7.9.2009"

echo "=============== build script ================"
echo image: "${IMAGE}"
echo image_tag: "${IMAGE_TAG}"
pwd

if [ -z "${IMAGE_TAG}" ]; then
    echo "Image tag must be specified. build ${IMAGE} Aborting..." >&2
    exit 1
fi

build_labeler_image() {
    export SRIOV_FEC_LABELER_IMAGE=$1

    sed -i "/FROM.*registry.*/c\FROM ${BASE_IMAGE}" \
        Dockerfile.labeler
    echo "labeler_image: ${SRIOV_FEC_LABELER_IMAGE}"

    pwd
    make image-sriov-fec-labeler

    echo "Labeler image build done"

    return 0
}

build_daemon_image() {
    export SRIOV_FEC_DAEMON_IMAGE=$1

    sed -i "/FROM.*registry.*/c\FROM ${BASE_IMAGE}" \
        Dockerfile.daemon

    echo "daemon_image: ${SRIOV_FEC_DAEMON_IMAGE}"

    pwd
    make image-sriov-fec-daemon

    echo "Daemon image build done"

    return 0
}

build_operator_image() {

    export SRIOV_FEC_OPERATOR_IMAGE=$1

    sed -i "/FROM.*registry.*/c\FROM ${BASE_IMAGE}" \
        Dockerfile

    echo "operator_image: ${SRIOV_FEC_OPERATOR_IMAGE}"

    pwd
    make image-sriov-fec-operator

    echo "Operator image build done"

    return 0
}

case ${IMAGE} in
    labeler)
        echo "Build image: labeler"
        build_labeler_image "${IMAGE_TAG}"
        ;;
    daemon)
        echo "build image: daemon"
        build_daemon_image "${IMAGE_TAG}"
        ;;
    operator)
        echo "build image: Operator"
        build_operator_image "${IMAGE_TAG}"
        ;;
    *)
        echo "Unsupported ARGS in ${image_build_file}: ${IMAGE}" >&2
        exit 1
        ;;
esac

exit 0
