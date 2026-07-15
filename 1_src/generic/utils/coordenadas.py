from pynput import keyboard
import pyautogui
import sys

def on_press(key):
    # Captura a posição com o Caps Lock
    if key == keyboard.Key.caps_lock:
        x, y = pyautogui.position()
        print(f"📍 Coordenada capturada: ({x}, {y})")
        # Opcional: print visual para confirmar que capturou
        sys.stdout.flush()

print("🚀 Monitor de Coordenadas Ativado!")
print("Pressione [Caps Lock] para capturar a posição do mouse.")
print("Pressione [Ctrl+C] no terminal para encerrar.")

# Usamos um Listener simples que roda enquanto o programa não for interrompido
with keyboard.Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando monitor de coordenadas...")
        sys.exit()