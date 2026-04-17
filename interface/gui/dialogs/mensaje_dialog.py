"""
Diálogos para mostrar mensajes al usuario.
"""
import customtkinter as ctk


def mostrar_mensaje(parent, mensaje: str, tipo: str = "info"):
    """Muestra un diálogo de mensaje simple."""
    
    colors = {
        "info": ("#3498db", "#2980b9"),
        "success": ("#27ae60", "#229954"),
        "error": ("#e74c3c", "#c0392b"),
        "warning": ("#f39c12", "#d68910")
    }
    
    fg, hover = colors.get(tipo, colors["info"])
    
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Mensaje")
    dialog.geometry("400x150")
    dialog.transient(parent)
    dialog.update()
    dialog.grab_set()
    
    label = ctk.CTkLabel(
        dialog,
        text=mensaje,
        font=ctk.CTkFont(size=14),
        wraplength=350
    )
    label.pack(expand=True, pady=20)
    
    btn = ctk.CTkButton(
        dialog,
        text="Aceptar",
        command=dialog.destroy,
        fg_color=fg,
        hover_color=hover,
        width=120
    )
    btn.pack(pady=10)


def mostrar_confirmacion(parent, mensaje: str, callback):
    """Muestra un diálogo de confirmación."""
    
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Confirmar")
    dialog.geometry("400x150")
    dialog.transient(parent)
    dialog.update()
    dialog.grab_set()
    
    label = ctk.CTkLabel(
        dialog,
        text=mensaje,
        font=ctk.CTkFont(size=14),
        wraplength=350
    )
    label.pack(expand=True, pady=20)
    
    frame_btn = ctk.CTkFrame(dialog, fg_color="transparent")
    frame_btn.pack(pady=10)
    
    def on_confirm():
        callback()
        dialog.destroy()
    
    btn_si = ctk.CTkButton(
        frame_btn,
        text="Sí",
        command=on_confirm,
        fg_color="#27ae60",
        hover_color="#229954",
        width=100
    )
    btn_si.pack(side="left", padx=5)
    
    btn_no = ctk.CTkButton(
        frame_btn,
        text="No",
        command=dialog.destroy,
        fg_color="#e74c3c",
        hover_color="#c0392b",
        width=100
    )
    btn_no.pack(side="left", padx=5)