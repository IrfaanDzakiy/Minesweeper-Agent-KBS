# User Manual
Untuk memainkan minesweeper, pengguna terlebih dahulu harus menginstall library numpy dan pygame dengan command
pip install numpy pygame

Kemudian, mengatur pengaturan dari permainan pada file ‘input.txt’. Baris pertama merupakan ukuran board yaitu. Baris kedua merupakan jumlah bomb, misalkan ‘n’. Sejumlah ‘n’ baris selanjutnya merupakan daftar koordinat bomb.  Sebagai contoh, dapat dilihat di bawah ini.


### Contoh masukan 
10 
8 
0, 6 
2, 2 
2, 4 
3, 3 
4, 2 
5, 6 
6, 2 
7, 8 
Baris pertama merupakan ukuran board yaitu 10 * 10. 
Baris kedua merupakan jumlah bomb yaitu 8. 
Delapan baris selanjutnya merupakan daftar koordinat bomb. 

Selanjutnya, jalankan program minesweeper.py untuk memantau gerakan agen pada konsol dengan command: 
python minesweeper.py

Atau jika ingin menggunakan GUI, jalankan dengan command:
python main.py
