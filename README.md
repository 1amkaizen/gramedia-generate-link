# gramedia-generate-link
Tools ini di gunakan untuk generate link affiliate gramedia

### persiapan
Sebelum menjalankan kodenya harus export dulu email dan password untuk login ke affiliate gramedia nya

```bash
export EMAIL="youremail@gmail.com"
export PASSWORD="yourpassword"
```

### cara menggunakan

```bash
python3 main.py -p 1
```

dengan flag `-p 1` ini akan menelusuri 1 halaman saja,dan jika menggunakan flag `-p 0` itu akan menelusuri semua halaman

