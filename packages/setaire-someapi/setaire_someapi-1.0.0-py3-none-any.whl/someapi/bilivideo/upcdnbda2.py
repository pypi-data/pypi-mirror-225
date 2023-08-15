'''
 # @ Author: tuweifeng
 # @ Create Time: 2022-07-12 21:44:19
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-02-23 18:26:29
 # @ Description:
 '''

import math
import os
from typing import List, Dict, Union
from threading import Thread
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import HTTPError
import retry


URL = "https://upos-sz-upcdnbda2.bilivideo.com"


class PutChunkTread(Thread):
    def __init__(self, thread_id, session: Session, cookies: RequestsCookieJar, size: int, uri: str, auth: str,  upload_id: str, filepath: str,
                 chunk_retry: int, chunk_timeout: int, chunk_retry_delay: int, chunk_size: int,
                 total_chunks: int, tasks: list, results: list, endpoint: str = "") -> None:
        super().__init__()
        self.thread_id = thread_id
        self.session = session
        self.cookies = cookies
        self.size = size
        self.uri = uri
        self.auth = auth
        self.upload_id = upload_id
        self.filepath = filepath
        self.chunk_retry = chunk_retry
        self.chunk_timeout = chunk_timeout
        self.chunk_retry_delay = chunk_retry_delay
        self.chunk_size = chunk_size
        self.endpoint = endpoint
        self.total_chunks = total_chunks
        self.tasks = tasks
        self.results = results

    def run(self) -> None:
        @retry.retry(exceptions=HTTPError, tries=self.chunk_retry, delay=self.chunk_retry_delay)
        def put_chunk(i, data):
            url = self.endpoint or URL
            res = self.session.put(
                url=url + "/" + self.uri,
                headers={
                    "x-upos-auth": self.auth,
                },
                params={
                    "partNumber": i + 1,
                    "uploadId": self.upload_id,
                    "chunk": i,
                    "chunks": self.total_chunks,
                    "size": len(data),
                    "start": i * self.chunk_size,
                    "end": i * self.chunk_size + len(data),
                    "total": self.size
                },
                data=data,
                cookies=self.cookies,
                timeout=self.chunk_timeout
            )
            print(
                f"[Thread-{self.thread_id}] put chunk: {i+1}/{self.total_chunks}", res)
            if int(res.status_code) != 200:
                raise HTTPError(f"partinfo error {res.status_code} {res.text}")
            self.results.append({'partNumber': index + 1, 'eTag': 'etag'})
        while self.tasks:
            index, data = self.tasks.pop()
            put_chunk(index, data)
        return super().run()


def upload_file(session: Session, cookies: RequestsCookieJar, uri: str, auth: str,  upload_id: str, filepath: str,
                chunk_retry: int, chunk_timeout: int, chunk_retry_delay: int, chunk_size: int,
                endpoint: str = "", threads: int = 2) -> List[Dict[str, Union[str, int]]]:
    size = os.path.getsize(filepath)

    total_chunks = math.ceil(size * 1.0 / chunk_size)
    index = 0
    tasks = []
    results = []

    with open(filepath, "rb") as f:
        data = f.read(chunk_size)
        while data:
            tasks.append((index, data))
            data = f.read(chunk_size)
            index += 1

    put_chunk_threads = []
    for i in range(threads):
        put_chunk_thread = PutChunkTread(i, session, cookies, size, uri, auth, upload_id, filepath, chunk_retry,
                                         chunk_timeout, chunk_retry_delay, chunk_size, total_chunks, tasks, results, endpoint)
        put_chunk_thread.start()
        put_chunk_threads.append(put_chunk_thread)

    for put_chunk_thread in put_chunk_threads:
        put_chunk_thread.join()

    assert len(results) == total_chunks
    return results


def post_partinfo(session: Session, cookies: RequestsCookieJar, uri: str, auth: str, name: str, upload_id: str, biz_id: int, partinfo: List[Dict[str, Union[str, int]]], endpoint: str = "") -> Response:
    url = endpoint or URL
    return session.post(
        url=url + "/" + uri,
        params={
            "output": "json",
            "name": name,
            "profile": "ugcupos/bup",
            "uploadId": upload_id,
            "biz_id": biz_id
        },
        json={"parts": partinfo},
        cookies=cookies,
        headers={
            "x-upos-auth": auth,
        })


def post_upload_id(session: Session, cookies: RequestsCookieJar, uri: str, auth: str, endpoint: str = "") -> Response:
    url = endpoint or URL
    return session.post(
        url=url + "/" + uri,
        params={
            "uploads": "",
            "output": "json"
        },
        cookies=cookies,
        headers={
            "x-upos-auth": auth
        })
