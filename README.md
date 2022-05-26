<img alt="logo" src="https://raw.githubusercontent.com/riecho14/Docker-Dendam-Si-Tikus/image_assets/logo.svg" width="400">

> Containerize Pygame with Docker.

## Nama dan NIM Anggota Kelompok
| Nama | NIM | Github |
| :---: | :---: | :---: |
| Mila Oktaviani             | 120140021 | [milaoktvni31](https://github.com/milaoktvni31)           |
| Bayu Nindioko              | 120140088 | [BayuNindioko](https://github.com/BayuNindioko)           |
| Naufal Rotif Dewanto       | 120140107 | [naufaldewanto37](https://github.com/naufaldewanto37)     |
| Azka Muzhaffar Sutawidjaja | 120140111 | [Zkaaaaaaa](https://github.com/Zkaaaaaaa)                 |
| Ericho Aldo Firano         | 120140119 | [riecho14](https://github.com/riecho14)                   |
| Andri Setiawan             | 120140191 | [Andri450](https://github.com/Andri450)                   |

## Dendam Si Tikus
#### Deskripsi Projek
Aplikasi ini merupakan permainan yang dibuat menggunakan library pygame tentang seekor tikus yang berusaha mengalahkan kucing dengan cara menyerang para kucing menggunakan racun. Permainan ini bertujuan untuk mendapatkan score sebanyak-banyaknya dengan cara menghindari dan mengalahkan para kucing yang berdatangan, nyawa tikus akan berkurang saat kucing menyentuh tikus. Permainan ini akan berakhir jika nyawa tikus telah habis.

## Cara Menjalankan Kontainer
Clone repositori ini atau [unduh disini](https://github.com/riecho14/Docker-Dendam-Si-Tikus/archive/refs/heads/main.zip) lalu pindahkan pygame scripts ke folder `~/Downloads` seperti pada gambar berikut:

![1](https://github.com/riecho14/Docker-Dendam-Si-Tikus/blob/a2eb90dc3131332f08d6dcbeefd0014c4d22d89b/1.png)

Selanjutnya buka terminal pada direktori folder tersebut lalu jalankan perintah build seperti berikut:

    make build-dendamsitikus

lalu pastikan ada repositori "dendamsitikus" pada docker, dengan cara jalankan command images untuk melihat daftar images pada local storage seperti berikut:

    docker images

Jika proses build telah selesai, jalankan perintah run seperti berikut:

untuk Windows

    make run-windows

untuk Linux

    make run-linux

untuk Mac

    make run-mac

Langkah terakhir yaitu menjalankan pygame melalui container yang telah kita buat dengan perintah seperti berikut:

    python3 -m main.py

## Video Demo Kontainer
[![LIHAT VIDEO DISINI](https://yt-embed.herokuapp.com/embed?v=ZRctNcWSxNk&ab)](https://www.youtube.com/watch?v=ZRctNcWSxNk&ab "Understandable Conversation Between Kobo and Crazy Dave 【Kobo Kanaeru Clip】")
