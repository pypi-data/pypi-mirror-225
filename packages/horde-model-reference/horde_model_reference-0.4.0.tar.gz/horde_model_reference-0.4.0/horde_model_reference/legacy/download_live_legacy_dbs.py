import pathlib

from loguru import logger

from horde_model_reference.legacy.legacy_download_manager import LegacyReferenceDownloadManager
from horde_model_reference.meta_consts import MODEL_REFERENCE_CATEGORY


def download_all_models(
    override_existing: bool = False,
    proxy_url: str = "",
) -> dict[MODEL_REFERENCE_CATEGORY, pathlib.Path | None]:
    reference_dm = LegacyReferenceDownloadManager(proxy_url=proxy_url)
    logger.warning("This method is deprecated. Use `download_all_model_references` instead.")
    return reference_dm.download_all_legacy_model_references(overwrite_existing=override_existing)


if __name__ == "__main__":
    reference_download_manager = LegacyReferenceDownloadManager()
    reference_download_manager.download_all_legacy_model_references(overwrite_existing=True)
