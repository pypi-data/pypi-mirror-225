# Waffle Profiler
Dx 인퍼런스 분석 툴  
Dx에 App을 설치하고 영상을 인퍼런스한 후 로그를 남긴다.  
남긴 로그와 영상 파일을 읽어와 화면에 인퍼런스 결과를 보여주는 기능도 제공한다.

# 사용법
## 설치
```bash
$ pip install dx-profiler
```

## sudo 등록
dx-profiler는 dx쪽에 영상을 복사하는 과정에서 sudo 권한이 필요하다.  
이를 위해 dx-profiler를 sudo에서 실행할 수 있도록 secure_path에 추가해준다.

예시)
```bash
$ which dx-profiler
/home/yoon/.cache/pypoetry/virtualenvs/dx-profiler-MxXHGb83-py3.10/bin/dx-profiler
$ sudo visudo
...

Defaults secure_path="/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/home/yoon/.cache/pypoetry/virtualenvs/dx-profiler-MxXHGb83-py3.10/bin"

...
```

## 인퍼런스
autocare_docker 레포를 clone한 후 dx-batch 브랜치로 checkout한다.  
docker compose up -d 로 dx 도커를 실행시킨 후 dx-profiler를 실행한다.

필요한 값
- 영상 파일 (-F)
- 앱 (-A)
- 로그 (-O)

예시)
```bash
$ sudo dx-profiler inference -F /mnt/hdd/videos/test_videos/helmet.mp4 --app ~/Downloads/aff0d790-8e15-47f4-874c-7320dc3673f9.zip -O log.txt
```

성공적으로 실행되면 영상 인퍼런스가 끝날때 까지 Waiting for EOS...를 출력하며
종료되면 Done.을 출력하고 종료된다.

## 영상확인
생성한 로그 기반으로 영상을 재생한다.

예시)
```bash
$ sudo dx-profiler profile -F log.txt
```
