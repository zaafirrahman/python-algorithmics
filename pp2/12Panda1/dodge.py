import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties

class GameMenghindar(ShowBase):
    def __init__(self):
        super().__init__()
        
        # 1. Atur Judul dan Ukuran Window
        properties = WindowProperties()
        properties.setTitle("Game Menghindar Asteroid 3D!")
        properties.setSize(800, 600)
        self.win.requestProperties(properties)
        
        # 2. Posisikan Kamera agar melihat dari atas (Bird-eye view)
        self.disableMouse() # Matikan kontrol kamera bawaan mouse
        self.camera.setPos(0, -20, 15)
        self.camera.lookAt(0, 0, 0)
        
        # 3. Bikin Player (Pesawat kita berbentuk Kotak)
        self.player = self.loader.loadModel("models/panda")
        self.player.reparentTo(self.render)
        self.player.setPos(0, 0, 0)
        self.player.setScale(0.25,0.25,0.25)
        
        # 4. Variabel Game
        self.skor = 0
        self.kecepatan_player = 15
        self.asteroid_list = []
        
        # 5. Setup Kontrol Keyboard (A ke kiri, D ke kanan)
        self.keys = {"kiri": False, "kanan": False}
        self.accept("a", self.set_key, ["kiri", True])
        self.accept("a-up", self.set_key, ["kiri", False])
        self.accept("d", self.set_key, ["kanan", True])
        self.accept("d-up", self.set_key, ["kanan", False])
        
        # 6. Jalankan Loop Game (Task)
        self.taskMgr.add(self.update_game, "UpdateGameTask")
        self.taskMgr.doMethodLater(0.5, self.spawn_asteroid, "SpawnAsteroidTask")

    # Fungsi untuk mendeteksi tombol ditekan/dilepas
    def set_key(self, key, value):
        self.keys[key] = value

    # Fungsi untuk memunculkan Asteroid (berbentuk Bola/Sphere)
    def spawn_asteroid(self, task):
        asteroid = self.loader.loadModel("models/smiley") # Pakai model bawaan smiley (bola)
        asteroid.reparentTo(self.render)
        
        # Muncul acak di koordinat X (kiri/kanan), dan di atas (Y menjauh)
        pos_x = random.uniform(-7, 7)
        asteroid.setPos(pos_x, 25, 0) 
        asteroid.setScale(0.8)
        
        self.asteroid_list.append(asteroid)
        return task.again # Ulangi task ini terus menerus

    # Loop Utama Game (Dijalankan setiap frame)
    def update_game(self, task):
        dt = globalClock.getDt() # Ambil delta time (waktu antar frame)
        
        # --- Pergerakan Player ---
        if self.keys["kiri"] and self.player.getX() > -7:
            self.player.setX(self.player.getX() - self.kecepatan_player * dt)
        if self.keys["kanan"] and self.player.getX() < 7:
            self.player.setX(self.player.getX() + self.kecepatan_player * dt)
            
        # --- Pergerakan & Logika Asteroid ---
        for asteroid in self.asteroid_list[:]:
            # Asteroid bergerak mendekati layar (Y berkurang)
            asteroid.setY(asteroid.getY() - 15 * dt)
            
            # Cek Tabrakan Sederhana (Jarak antara player dan asteroid)
            jarak = self.player.getDistance(asteroid)
            if jarak < 1.2:
                print(f"GAME OVER! Skor Akhir Kamu: {self.skor}")
                self.userExit() # Keluar dari game
                
            # Jika asteroid lewat dari layar, hapus dan tambah skor
            if asteroid.getY() < -5:
                self.asteroid_list.remove(asteroid)
                asteroid.removeNode()
                self.skor += 1
                print(f"Skor: {self.skor}")
                
        return task.cont

# Jalankan Gamenya!
game = GameMenghindar()
game.run()