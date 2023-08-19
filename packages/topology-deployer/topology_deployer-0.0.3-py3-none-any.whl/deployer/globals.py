from pathlib import Path

OP_CREATE = 1
OP_DELETE = 2

OP = OP_CREATE
DRY_RUN = False
NO_NETWORK = False
NO_VM = False
RECREATE_NW = False
PRINT_NETWORK = False
PRINT_VM = False

LIBVIRT_BASE_PATH = Path('/var/lib/libvirt')
LIBVIRT_IMAGES = LIBVIRT_BASE_PATH.joinpath('images')
LIBVIRT_TEMPLATES = LIBVIRT_IMAGES.joinpath('templates')
LIBVIRT_QEMU_BASE = Path('/etc/libvirt/qemu')
LIBVIRT_QEMU_NW = LIBVIRT_QEMU_BASE.joinpath('networks')

UBUNTU_TEMPLATE = LIBVIRT_TEMPLATES.joinpath('ubuntu-22.04-server.qcow2')
NAT_NW_BASE = Path.home().joinpath('.topology/bridges')
