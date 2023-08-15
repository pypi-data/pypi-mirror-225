import os
import shutil
import tempfile
from pathlib import Path

import pytest

from tetra_hub.client import (
    UserError,
    _assert_is_valid_zipped_model,
    _make_zipped_model_compatible,
)


def create_sample_mlmodelc(modelDir: Path, include_assemble_json: bool = False):
    Path(modelDir).mkdir(parents=True)
    Path(modelDir / "model.espresso.net").touch()
    Path(modelDir / "model.espresso.shape").touch()
    Path(modelDir / "model.espresso.weights").touch()
    if include_assemble_json:
        Path(modelDir / "assemble.json").touch()


def test_valid_zipped_mlmodelc():
    #  1. <filepath>/foo.mlmodelc/assemble.json in case of pipeline model
    #  2. <filepath>/foo.mlmodelc/model.espresso.net or
    #  3. <filepath>/foo.mlmodelc/model0/model.espresso.net in case of pipeline model

    mlmodelc_name = "myModel.mlmodelc"
    # Case 1:
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 2
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 3
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / "myModel.mlmodelc"
        pipelinePath = Path(modelDir) / "model0"
        create_sample_mlmodelc(pipelinePath)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Unsupported: model.espresso.net / assemble.json present
    # with flat directory structure i.e. model.zip -> model.espresso.net
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(str(zipPath), "zip", root_dir=modelDir, base_dir="./")
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Valid .mlmodelc within zip with no model.espresso.net/assemble.json
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        # Make an invalid model
        modelDir = Path(baseDir) / mlmodelc_name
        Path(modelDir).mkdir()
        Path(modelDir / "bad_file").touch()

        # Check that this fails
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_valid_zipped_mlpackage():
    # <dirpath>/foo.mlpackage/ in case of zipped mlpackage

    mlpackage_name = "myModel.mlpackage"
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlpackage_name
        os.makedirs(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlpackage_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_make_mlmodelc_compatible_zip_does_not_zip_zip():
    model_name = "myModel.mlmodelc"
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / model_name
        create_sample_mlmodelc(model_dir)

        zip_base_path = Path(base_dir) / "my_model_archive"
        zip_path = shutil.make_archive(
            str(zip_base_path), "zip", root_dir=base_dir, base_dir=model_name
        )

        with tempfile.NamedTemporaryFile(suffix=".mlmodelc.zip") as model_zip_tempfile:
            mlmodelc_zip_path = _make_zipped_model_compatible(
                zip_path, model_zip_tempfile.name, ".mlmodelc"
            )
            assert mlmodelc_zip_path == zip_path


def test_make_mlmodelc_compatible_zip_zips_dir():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)

        model_output_path = str(Path(base_dir, "output_model_dir"))
        os.makedirs(model_output_path)
        zipfile_path = _make_zipped_model_compatible(
            str(model_dir), model_output_path, ".mlmodelc"
        )
        assert zipfile_path == os.path.join(model_output_path, "myModel.mlmodelc.zip")
        _assert_is_valid_zipped_model(zipfile_path)


def test_make_mlmodelc_compatible_zip_zips_dir_removing_additional_dirs():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)
        Path(os.path.join(base_dir, "__MACOS__")).mkdir(parents=True)
        Path(os.path.join(base_dir, "some_random_file")).touch()

        zipped_file_path = shutil.make_archive(
            os.path.join(base_dir, "test_model.mlmodelc"), "zip", root_dir=base_dir
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            zipfile_path = _make_zipped_model_compatible(
                zipped_file_path, tmp_dir, ".mlmodelc"
            )
            assert zipfile_path == str(os.path.join(tmp_dir, "myModel.mlmodelc.zip"))
            _assert_is_valid_zipped_model(zipfile_path)
