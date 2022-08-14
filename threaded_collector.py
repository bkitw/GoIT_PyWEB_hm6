import sys
from pathlib import Path
import concurrent.futures

files = {
    'KNOWN_EXT':
        {
            'EXE': [],
            'TORRENT': [],
            'PY': [],
            'JPEG': [],
            'JPG': [],
            'PNG': [],
            'SVG': [],
            'BMP': [],
            'MP3': [],
            'OGG': [],
            'WAV': [],
            'FLAC': [],
            'AMR': [],
            'MKV': [],
            '3GP': [],
            'MP4': [],
            'MOV': [],
            'AVI': [],
            'DOC': [],
            'DOCX': [],
            'TXT': [],
            'PDF': [],
            'XLSX': [],
            'PPTX': [],
            'MPP': [],
            'ZIP': [],
            'RAR': [],
            'ISO': [],
            'GZ': [],
            'TAR': [],
        },
    'UNKNOWN_EXT': [],
    'FOLDERS': [],
}


def extract_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def sorter(folder_for_scan: Path) -> dict:
    files = {
        'KNOWN_EXT':
            {
                'EXE': [],
                'TORRENT': [],
                'PY': [],
                'JPEG': [],
                'JPG': [],
                'PNG': [],
                'SVG': [],
                'BMP': [],
                'MP3': [],
                'OGG': [],
                'WAV': [],
                'FLAC': [],
                'AMR': [],
                'MKV': [],
                '3GP': [],
                'MP4': [],
                'MOV': [],
                'AVI': [],
                'DOC': [],
                'DOCX': [],
                'TXT': [],
                'PDF': [],
                'XLSX': [],
                'PPTX': [],
                'MPP': [],
                'ZIP': [],
                'RAR': [],
                'ISO': [],
                'GZ': [],
                'TAR': [],
            },
        'UNKNOWN_EXT': [],
        'FOLDERS': [],
    }
    results = []
    folders = [folder_for_scan]
    while folders:
        new_folders = []
        for folder in folders:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for item in folder.iterdir():
                    result = executor.submit(ext_handler, item, folder).result()
                    results.append(result)
                    if result['type'] == 'folder':
                        new_folders.append(result['item'])

        folders = []
        if new_folders:
            folders = new_folders

    for file in results:
        if file['type'] == 'folder':
            files['FOLDERS'].append(file['item'])
        elif file['type'] == 'file' and file['extension'] == '':
            files['UNKNOWN_EXT'].append(file['item'])
        elif file['type'] == 'file':
            try:
                files['KNOWN_EXT'][file['extension']].append(file['item'])
            except KeyError:
                files['UNKNOWN_EXT'].append(file['item'])

    return files


def ext_handler(item, folder):
    data = {'type': '',
            'extension': '',
            'item': item}
    if item.is_dir():
        if item.name not in ('archives', 'audio', 'video', 'documents', 'images',
                             'uncertain_types', 'torrents', 'applications',
                             'python_files(scripts'):
            data['type'] = 'folder'

    else:
        data['type'] = 'file'
        ext = extract_extension(item.name)
        fullname = folder / item.name
        data['item'] = fullname
        if ext:
            data['extension'] = ext

    return data


