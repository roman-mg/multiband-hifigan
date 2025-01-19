import os
import urllib.request
import tarfile
from tqdm import tqdm


def download(
  output_folder: str,
  url: str = "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"
  ) -> None:
    print("Downloading LJSpeech-1.1 ...")
    chunk_size = 8192
    archive_name = "LJSpeech-1.1.tar.bz2"
    archive_path = os.path.join(output_folder, archive_name)

    os.makedirs(output_folder, exist_ok=True)
    response = urllib.request.urlopen(url)
    file_size = int(response.headers.get('Content-Length', 0))

    with open(archive_path, "wb") as file, tqdm(
        desc=archive_name,
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            file.write(chunk)
            progress_bar.update(len(chunk))

    with tarfile.open(archive_path, "r:bz2") as tar:
        tar.extractall(path=output_folder)

    os.remove(archive_path)
    print("Done.")


if __name__ == "__main__":
    download("/content/multiband-hifigan/datasets")
