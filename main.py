import asyncio
import aioshutil
import sys
from tqdm import tqdm
import time
from pathlib import Path
from aiopath import AsyncPath
import threaded_collector as collector
from normalize import normalize


async def handle_media(filename: Path, target_folder: Path):
    filename = AsyncPath(filename)
    target_folder = AsyncPath(target_folder)
    await target_folder.mkdir(exist_ok=True, parents=True)

    await filename.replace(target_folder / normalize(filename.name))


async def handle_archives(filename: Path, target_folder: Path):
    filename = AsyncPath(filename)
    target_folder = AsyncPath(target_folder)
    await target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file = AsyncPath(folder_for_file)
    await folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        filename = Path(filename)
        folder_for_file = Path(folder_for_file)
        await aioshutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except aioshutil.Error:
        print(f'\tDIRECTED BY:')
        print('\tRobert B Weide')
        folder_for_file = AsyncPath(folder_for_file)
        await folder_for_file.rmdir()
    filename = AsyncPath(filename)
    await filename.unlink()


async def handle_folders(folder: Path):
    folder = AsyncPath(folder)
    try:
        await folder.rmdir()
    except OSError:
        print(f'Oops, the things gone wrong with -- {folder}')


class Images:
    collection_of_images = {}

    def __init__(self, files):
        self.collection_of_images = {'images': [
            files['KNOWN_EXT']['JPEG'],
            files['KNOWN_EXT']['BMP'],
            files['KNOWN_EXT']['PNG'],
            files['KNOWN_EXT']['JPG'],
            files['KNOWN_EXT']['SVG'],
        ]}

    async def thread_image_loop(self, folder: Path):

        futures = []
        for collection, values in self.collection_of_images.items():
            for ext in values:
                for file in ext:
                    futures.append(handle_media(file, folder / collection))
        await asyncio.gather(*futures)


...


class Audio:
    collection_of_audio = {}

    def __init__(self, files):
        self.collection_of_audio = {'audio': [
            files['KNOWN_EXT']['MP3'],
            files['KNOWN_EXT']['WAV'],
            files['KNOWN_EXT']['AMR'],
            files['KNOWN_EXT']['OGG'],
            files['KNOWN_EXT']['FLAC'],
        ]}

    async def thread_audio_loop(self, folder: Path):

        futures = []
        for collection, values in self.collection_of_audio.items():
            for ext in values:
                for file in ext:
                    futures.append(handle_media(file, folder / collection))
        await asyncio.gather(*futures)


...


class Video:
    collection_of_video = {}

    def __init__(self, files):
        self.collection_of_video = {'video': [
            files['KNOWN_EXT']['3GP'],
            files['KNOWN_EXT']['MP4'],
            files['KNOWN_EXT']['MOV'],
            files['KNOWN_EXT']['MKV'],
            files['KNOWN_EXT']['AVI'],
        ]}

    async def thread_video_loop(self, folder: Path):
        futures = []
        for collection, values in self.collection_of_video.items():
            for ext in values:
                for file in ext:
                    futures.append(handle_media(file, folder / collection))
        await asyncio.gather(*futures)


class Documents:
    collection_of_documents = {}

    def __init__(self, files):
        self.collection_of_documents = {'documents': [
            files['KNOWN_EXT']['DOC'],
            files['KNOWN_EXT']['DOCX'],
            files['KNOWN_EXT']['MPP'],
            files['KNOWN_EXT']['TXT'],
            files['KNOWN_EXT']['XLSX'],
            files['KNOWN_EXT']['PPTX'],
            files['KNOWN_EXT']['PDF'],
        ]}

    async def thread_documents_loop(self, folder: Path):
        futures = []
        for collection, values in self.collection_of_documents.items():
            for ext in values:
                for file in ext:
                    futures.append(handle_media(file, folder / collection))
        await asyncio.gather(*futures)


class TorrentPythonExe:
    collection_of_torrent_python_exe = {}

    def __init__(self, files):
        self.collection_of_torrent_python_exe = {
            'torrents':
                files['KNOWN_EXT']['TORRENT'],
            'python_scripts':
                files['KNOWN_EXT']['PY'],
            'applications':
                files['KNOWN_EXT']['EXE']
        }

    async def thread_tpe_loop(self, folder: Path):
        futures = []
        for collection, values in self.collection_of_torrent_python_exe.items():
            for file in values:
                futures.append(handle_media(file, folder / collection))
        await asyncio.gather(*futures)


class AnotherTypes:

    def __init__(self, files):
        self.unknown_files = files['UNKNOWN_EXT']

    async def thread_unknown_loop(self, folder: Path):
        futures = []
        for file in self.unknown_files:
            futures.append(handle_media(file, folder / 'uncertain_types'))
        await asyncio.gather(*futures)


class Archives:
    collection_of_archives = {}

    def __init__(self, files):
        self.collection_of_archives = {'archives': [
            files['KNOWN_EXT']['GZ'],
            files['KNOWN_EXT']['RAR'],
            files['KNOWN_EXT']['ZIP'],
            files['KNOWN_EXT']['ISO'],
            files['KNOWN_EXT']['TAR'],

        ]}

    async def thread_archive_loop(self, folder: Path):
        futures = []
        for collection, values in self.collection_of_archives.items():
            for ext in values:
                for file in ext:
                    futures.append(handle_archives(file, folder / collection))
        await asyncio.gather(*futures)


...


class Folders:
    def __init__(self, files):
        self.folders = files['FOLDERS'][::-1]

    async def thread_for_folders(self, folder: Path):
        futures = []
        for folder in self.folders:
            futures.append(handle_folders(folder))
        await asyncio.gather(*futures)


def main(folder: Path):
    files = collector.sorter(folder)

    images_object = Images(files)
    asyncio.run(images_object.thread_image_loop(folder))

    ...
    audio_object = Audio(files)
    asyncio.run(audio_object.thread_audio_loop(folder))

    ...
    video_object = Video(files)
    asyncio.run(video_object.thread_video_loop(folder))

    ...
    documents_object = Documents(files)
    asyncio.run(documents_object.thread_documents_loop(folder))

    ...
    three_in_one_object = TorrentPythonExe(files)
    asyncio.run(three_in_one_object.thread_tpe_loop(folder))

    ...
    unknown_type_object = AnotherTypes(files)
    asyncio.run(unknown_type_object.thread_unknown_loop(folder))
    ...
    archives_object = Archives(files)
    asyncio.run(archives_object.thread_archive_loop(folder))
    ...

    folders_object = Folders(files)
    asyncio.run(folders_object.thread_for_folders(folder))
    ...
    return files


if __name__ == '__main__':
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Sorting will start in folder -- {folder_for_scan.resolve()}')
        data = main(folder_for_scan.resolve())
        print('Names of all files was changed from cyrillic to latin.')
        for i in tqdm(data, desc="Sorting progress", colour='green'):
            time.sleep(0.5)
        for j in tqdm(data['KNOWN_EXT'], desc="Sorting known files", colour="blue"):
            time.sleep(0.1)
        for k in tqdm(data['UNKNOWN_EXT'], desc="Sorting unknown files", colour="magenta"):
            time.sleep(0.1)
        time.sleep(2)
        print('Sorting finished!')
