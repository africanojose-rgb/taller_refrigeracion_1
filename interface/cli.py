import typer
from typing_extensions import Annotated
from datetime import date
from infrastructure.database import init_db, get_session
from infrastructure.repositories.cliente_repository_impl import ClienteRepositoryImpl
from infrastructure.repositories.equipo_repository_impl import EquipoRepositoryImpl
from infrastructure.repositories.orden_repository_impl import OrdenRepositoryImpl
from infrastructure.repositories.tecnico_repository_impl import TecnicoRepositoryImpl
from application.use_cases.cliente_use_cases import ClienteUseCases
from application.use_cases.equipo_use_cases import EquipoUseCases
from application.use_cases.orden_use_cases import OrdenUseCases
from application.use_cases.tecnico_use_cases import TecnicoUseCases
from application.use_cases.reporte_use_cases import ReporteUseCases
from application.dto import (
    ClienteCreateDTO, ClienteUpdateDTO,
    EquipoCreateDTO, EquipoUpdateDTO,
    OrdenCreateDTO, OrdenUpdateDTO, OrdenCompletarDTO,
    TecnicoCreateDTO, TecnicoUpdateDTO
)


app = typer.Typer(help="Sistema de Gestión de Taller de Refrigeración")


class ServiceContainer:
    def __init__(self):
        init_db()
        session = get_session()
        self.cliente_repo = ClienteRepositoryImpl(session)
        self.equipo_repo = EquipoRepositoryImpl(session)
        self.orden_repo = OrdenRepositoryImpl(session)
        self.tecnico_repo = TecnicoRepositoryImpl(session)
        
        self.cliente_use_cases = ClienteUseCases(self.cliente_repo)
        self.equipo_use_cases = EquipoUseCases(self.equipo_repo)
        self.orden_use_cases = OrdenUseCases(self.orden_repo)
        self.tecnico_use_cases = TecnicoUseCases(self.tecnico_repo)
        self.reporte_use_cases = ReporteUseCases(
            self.cliente_repo, self.equipo_repo, self.orden_repo, self.tecnico_repo
        )


services = ServiceContainer()


@app.command()
def crear_cliente(
    nombre: str = typer.Argument(..., help="Nombre del cliente"),
    telefono: str = typer.Argument(..., help="Teléfono del cliente"),
    direccion: str = typer.Option("", "--direccion", "-d", help="Dirección del cliente"),
    email: str = typer.Option("", "--email", "-e", help="Email del cliente")
):
    dto = ClienteCreateDTO(nombre=nombre, telefono=telefono, direccion=direccion or None, email=email or None)
    cliente = services.cliente_use_cases.crear_cliente(dto)
    typer.echo(f"✓ Cliente creado: ID {cliente.id} - {cliente.nombre}")


@app.command()
def listar_clientes():
    clientes = services.cliente_use_cases.listar_clientes()
    if not clientes:
        typer.echo("No hay clientes registrados.")
        return
    for c in clientes:
        typer.echo(f"[{c.id}] {c.nombre} | Tel: {c.telefono} | Email: {c.email or '-'}")


@app.command()
def buscar_cliente(nombre: str = typer.Argument(..., help="Nombre a buscar")):
    resultados = services.cliente_use_cases.buscar_clientes(nombre)
    if not resultados:
        typer.echo(f"No se encontraron clientes con '{nombre}'")
        return
    for c in resultados:
        typer.echo(f"[{c.id}] {c.nombre} | Tel: {c.telefono}")


@app.command()
def actualizar_cliente(
    id: int = typer.Argument(..., help="ID del cliente"),
    nombre: str = typer.Option(None, "--nombre", "-n", help="Nuevo nombre"),
    telefono: str = typer.Option(None, "--telefono", "-t", help="Nuevo teléfono"),
    direccion: str = typer.Option(None, "--direccion", "-d", help="Nueva dirección"),
    email: str = typer.Option(None, "--email", "-e", help="Nuevo email")
):
    dto = ClienteUpdateDTO(
        nombre=nombre if nombre else None,
        telefono=telefono if telefono else None,
        direccion=direccion if direccion else None,
        email=email if email else None
    )
    try:
        cliente = services.cliente_use_cases.actualizar_cliente(id, dto)
        typer.echo(f"✓ Cliente actualizado: {cliente.nombre}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def eliminar_cliente(id: int = typer.Argument(..., help="ID del cliente")):
    if services.cliente_use_cases.eliminar_cliente(id):
        typer.echo(f"✓ Cliente {id} eliminado")
    else:
        typer.echo(f"✗ Cliente {id} no encontrado", err=True)


@app.command()
def crear_equipo(
    tipo: str = typer.Argument(..., help="Tipo de equipo"),
    marca: str = typer.Argument(..., help="Marca del equipo"),
    cliente_id: int = typer.Argument(..., min=1, help="ID del cliente"),
    modelo: str = typer.Option("", "--modelo", "-m", help="Modelo del equipo"),
    serial: str = typer.Option("", "--serial", "-s", help="Número de serie")
):
    dto = EquipoCreateDTO(tipo_equipo=tipo, marca=marca, modelo=modelo or None, serial=serial or None, cliente_id=cliente_id)
    try:
        equipo = services.equipo_use_cases.crear_equipo(dto)
        typer.echo(f"✓ Equipo creado: ID {equipo.id} - {equipo.tipo_equipo} {equipo.marca}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def listar_equipos():
    equipos = services.equipo_use_cases.listar_equipos()
    if not equipos:
        typer.echo("No hay equipos registrados.")
        return
    for e in equipos:
        typer.echo(f"[{e.id}] {e.tipo_equipo} {e.marca} {e.modelo or ''} | Serial: {e.serial or '-'}")


@app.command()
def listar_equipos_cliente(cliente_id: int = typer.Argument(..., help="ID del cliente")):
    equipos = services.equipo_use_cases.listar_equipos_por_cliente(cliente_id)
    if not equipos:
        typer.echo(f"El cliente {cliente_id} no tiene equipos.")
        return
    for e in equipos:
        typer.echo(f"[{e.id}] {e.tipo_equipo} {e.marca} {e.modelo or ''}")


@app.command()
def actualizar_equipo(
    id: int = typer.Argument(..., help="ID del equipo"),
    tipo: str = typer.Option(None, "--tipo", "-t", help="Nuevo tipo"),
    marca: str = typer.Option(None, "--marca", "-m", help="Nueva marca"),
    modelo: str = typer.Option(None, "--modelo", help="Nuevo modelo"),
    serial: str = typer.Option(None, "--serial", "-s", help="Nuevo serial")
):
    dto = EquipoUpdateDTO(
        tipo_equipo=tipo if tipo else None,
        marca=marca if marca else None,
        modelo=modelo if modelo else None,
        serial=serial if serial else None
    )
    try:
        equipo = services.equipo_use_cases.actualizar_equipo(id, dto)
        typer.echo(f"✓ Equipo actualizado: {equipo.tipo_equipo} {equipo.marca}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def eliminar_equipo(id: int = typer.Argument(..., help="ID del equipo")):
    if services.equipo_use_cases.eliminar_equipo(id):
        typer.echo(f"✓ Equipo {id} eliminado")
    else:
        typer.echo(f"✗ Equipo {id} no encontrado", err=True)


@app.command()
def buscar_equipo(serial: str = typer.Argument(..., help="Número de serie")):
    equipo = services.equipo_use_cases.buscar_por_serial(serial)
    if equipo:
        typer.echo(f"[{equipo.id}] {equipo.tipo_equipo} {equipo.marca} {equipo.modelo or ''} | Cliente ID: {equipo.cliente_id}")
    else:
        typer.echo(f"✗ Equipo con serial '{serial}' no encontrado", err=True)


@app.command()
def crear_tecnico(
    nombre: str = typer.Argument(..., help="Nombre del técnico"),
    especialidad: str = typer.Argument(..., help="Especialidad"),
    telefono: str = typer.Argument(..., help="Teléfono")
):
    dto = TecnicoCreateDTO(nombre=nombre, especialidad=especialidad, telefono=telefono)
    tecnico = services.tecnico_use_cases.crear_tecnico(dto)
    typer.echo(f"✓ Técnico creado: ID {tecnico.id} - {tecnico.nombre}")


@app.command()
def listar_tecnicos():
    tecnicos = services.tecnico_use_cases.listar_tecnicos()
    if not tecnicos:
        typer.echo("No hay técnicos registrados.")
        return
    for t in tecnicos:
        typer.echo(f"[{t.id}] {t.nombre} | Especialidad: {t.especialidad} | Tel: {t.telefono}")


@app.command()
def actualizar_tecnico(
    id: int = typer.Argument(..., help="ID del técnico"),
    nombre: str = typer.Option(None, "--nombre", "-n", help="Nuevo nombre"),
    especialidad: str = typer.Option(None, "--especialidad", "-e", help="Nueva especialidad"),
    telefono: str = typer.Option(None, "--telefono", "-t", help="Nuevo teléfono")
):
    dto = TecnicoUpdateDTO(
        nombre=nombre if nombre else None,
        especialidad=especialidad if especialidad else None,
        telefono=telefono if telefono else None
    )
    try:
        tecnico = services.tecnico_use_cases.actualizar_tecnico(id, dto)
        typer.echo(f"✓ Técnico actualizado: {tecnico.nombre}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def eliminar_tecnico(id: int = typer.Argument(..., help="ID del técnico")):
    if services.tecnico_use_cases.eliminar_tecnico(id):
        typer.echo(f"✓ Técnico {id} eliminado")
    else:
        typer.echo(f"✗ Técnico {id} no encontrado", err=True)


@app.command()
def buscar_tecnico(especialidad: str = typer.Argument(..., help="Especialidad a buscar")):
    resultados = services.tecnico_use_cases.buscar_por_especialidad(especialidad)
    if not resultados:
        typer.echo(f"No se encontraron técnicos con especialidad '{especialidad}'")
        return
    for t in resultados:
        typer.echo(f"[{t.id}] {t.nombre} | Tel: {t.telefono}")


@app.command()
def crear_orden(
    equipo_id: int = typer.Argument(..., min=1, help="ID del equipo"),
    tecnico_id: int = typer.Argument(..., min=1, help="ID del técnico"),
    diagnostico: str = typer.Option("", "--diagnostico", help="Diagnóstico inicial"),
    costo: float = typer.Option(0.0, "--costo", help="Costo estimado")
):
    dto = OrdenCreateDTO(diagnostico=diagnostico or None, costo=costo, equipo_id=equipo_id, tecnico_id=tecnico_id)
    try:
        orden = services.orden_use_cases.crear_orden(dto)
        typer.echo(f"✓ Orden creada: ID {orden.id} - Estado: {orden.estado.value}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def listar_ordenes():
    ordenes = services.orden_use_cases.listar_ordenes()
    if not ordenes:
        typer.echo("No hay órdenes registradas.")
        return
    for o in ordenes:
        typer.echo(f"[{o.id}] Estado: {o.estado.value} | Costo: ${o.costo} | Fecha: {o.fecha_ingreso}")


@app.command()
def listar_ordenes_estado(estado: str = typer.Argument(..., help="Estado: pendiente, en_proceso, terminado, cancelado")):
    try:
        ordenes = services.orden_use_cases.listar_por_estado(estado)
        if not ordenes:
            typer.echo(f"No hay órdenes en estado '{estado}'")
            return
        for o in ordenes:
            typer.echo(f"[{o.id}] Costo: ${o.costo} | Fecha: {o.fecha_ingreso}")
    except ValueError:
        typer.echo(f"✗ Estado inválido: {estado}", err=True)


@app.command()
def historial_cliente(cliente_id: int = typer.Argument(..., help="ID del cliente")):
    ordenes = services.orden_use_cases.listar_por_cliente(cliente_id)
    if not ordenes:
        typer.echo(f"El cliente {cliente_id} no tiene historial.")
        return
    typer.echo(f"=== Historial del Cliente {cliente_id} ===")
    for o in ordenes:
        typer.echo(f"[{o.id}] {o.fecha_ingreso} | {o.estado.value} | ${o.costo} | {o.diagnostico[:30] if o.diagnostico else 'Sin diagnóstico'}...")


@app.command()
def iniciar_orden(orden_id: int = typer.Argument(..., help="ID de la orden")):
    try:
        orden = services.orden_use_cases.iniciar_orden(orden_id)
        typer.echo(f"✓ Orden {orden_id} iniciada. Estado: {orden.estado.value}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def completar_orden(
    orden_id: int = typer.Argument(..., help="ID de la orden"),
    solucion: str = typer.Option(..., "--solucion", "-s", help="Solución aplicada"),
    costo: float = typer.Option(..., "--costo", "-c", help="Costo final")
):
    dto = OrdenCompletarDTO(solucion=solucion, costo=costo)
    try:
        orden = services.orden_use_cases.completar_orden(orden_id, dto)
        typer.echo(f"✓ Orden {orden_id} completada. Costo final: ${orden.costo}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def actualizar_orden(
    orden_id: int = typer.Argument(..., help="ID de la orden"),
    diagnostico: str = typer.Option(None, "--diagnostico", "-d", help="Nuevo diagnóstico"),
    costo: float = typer.Option(None, "--costo", "-c", help="Nuevo costo")
):
    dto = OrdenUpdateDTO(
        diagnostico=diagnostico if diagnostico else None,
        costo=costo if costo else None
    )
    try:
        orden = services.orden_use_cases.actualizar_orden(orden_id, dto)
        typer.echo(f"✓ Orden actualizada. Estado: {orden.estado.value}")
    except ValueError as e:
        typer.echo(f"✗ Error: {e}", err=True)


@app.command()
def eliminar_orden(orden_id: int = typer.Argument(..., help="ID de la orden")):
    if services.orden_use_cases.eliminar_orden(orden_id):
        typer.echo(f"✓ Orden {orden_id} eliminada")
    else:
        typer.echo(f"✗ Orden {orden_id} no encontrada", err=True)


@app.command()
def ver_orden(orden_id: int = typer.Argument(..., help="ID de la orden")):
    orden = services.orden_use_cases.obtener_orden(orden_id)
    if not orden:
        typer.echo(f"✗ Orden {orden_id} no encontrada", err=True)
        return
    typer.echo(f"=== Orden #{orden.id} ===")
    typer.echo(f"Fecha ingreso: {orden.fecha_ingreso}")
    typer.echo(f"Fecha entrega: {orden.fecha_entrega or 'Pendiente'}")
    typer.echo(f"Estado: {orden.estado.value}")
    typer.echo(f"Diagnóstico: {orden.diagnostico or 'Sin diagnóstico'}")
    typer.echo(f"Solución: {orden.solucion or 'Sin solución'}")
    typer.echo(f"Costo: ${orden.costo}")
    typer.echo(f"Equipo ID: {orden.equipo_id}")
    typer.echo(f"Técnico ID: {orden.tecnico_id}")


@app.command()
def reporte_general():
    """Muestra estadísticas generales del taller."""
    stats = services.reporte_use_cases.obtener_estadisticas_generales()
    typer.echo("=== ESTADÍSTICAS GENERALES ===")
    typer.echo(f"Total Clientes: {stats.total_clientes}")
    typer.echo(f"Total Equipos: {stats.total_equipos}")
    typer.echo(f"Total Órdenes: {stats.total_ordenes}")
    typer.echo(f"Órdenes Pendientes: {stats.ordenes_pendientes}")
    typer.echo(f"Órdenes en Proceso: {stats.ordenes_en_proceso}")
    typer.echo(f"Órdenes Terminadas: {stats.ordenes_terminadas}")
    typer.echo(f"Ingreso Total: ${stats.ingreso_total:.2f}")
    typer.echo(f"Promedio por Orden: ${stats.promedio_orden:.2f}")


@app.command()
def reporte_cliente(cliente_id: int = typer.Argument(..., help="ID del cliente")):
    """Muestra reporte detallado de un cliente."""
    reporte = services.reporte_use_cases.obtener_reporte_cliente(cliente_id)
    if not reporte:
        typer.echo(f"✗ Cliente {cliente_id} no encontrado", err=True)
        return
    typer.echo(f"=== REPORTE CLIENTE #{reporte.cliente_id} ===")
    typer.echo(f"Nombre: {reporte.nombre}")
    typer.echo(f"Equipos Registrados: {reporte.total_equipos}")
    typer.echo(f"Órdenes de Servicio: {reporte.total_ordenes}")
    typer.echo(f"Gasto Total: ${reporte.gasto_total:.2f}")


@app.command()
def reporte_tecnico(tecnico_id: int = typer.Argument(..., help="ID del técnico")):
    """Muestra rendimiento de un técnico."""
    reporte = services.reporte_use_cases.obtener_reporte_tecnico(tecnico_id)
    if not reporte:
        typer.echo(f"✗ Técnico {tecnico_id} no encontrado", err=True)
        return
    typer.echo(f"=== REPORTE TÉCNICO #{reporte.tecnico_id} ===")
    typer.echo(f"Nombre: {reporte.nombre}")
    typer.echo(f"Especialidad: {reporte.especialidad}")
    typer.echo(f"Órdenes Completadas: {reporte.ordenes_completadas}")
    typer.echo(f"Ingreso Generado: ${reporte.ingreso_total:.2f}")


@app.command()
def top_clientes(limite: int = typer.Option(10, "--limite", "-l", help="Número de clientes")):
    """Lista los clientes con mayor gasto."""
    top = services.reporte_use_cases.listar_top_clientes(limite)
    if not top:
        typer.echo("No hay datos de clientes.")
        return
    typer.echo(f"=== TOP {len(top)} CLIENTES ===")
    for i, r in enumerate(top, 1):
        typer.echo(f"{i}. {r.nombre} - ${r.gasto_total:.2f} ({r.total_ordenes} órdenes)")


@app.command()
def top_tecnicos(limite: int = typer.Option(10, "--limite", "-l", help="Número de técnicos")):
    """Lista los técnicos con más órdenes completadas."""
    top = services.reporte_use_cases.listar_top_tecnicos(limite)
    if not top:
        typer.echo("No hay datos de técnicos.")
        return
    typer.echo(f"=== TOP {len(top)} TÉCNICOS ===")
    for i, r in enumerate(top, 1):
        typer.echo(f"{i}. {r.nombre} - {r.ordenes_completadas} órdenes, ${r.ingreso_total:.2f}")


if __name__ == "__main__":
    app()