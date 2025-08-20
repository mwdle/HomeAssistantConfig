import sys
from datetime import datetime

# Add the pyscript_modules directory to Python's module search path (`compose.yaml` is configured to mount contents of `python_modules` into container automatically) 
# See https://hacs-pyscript.readthedocs.io/en/latest/reference.html#importing
if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")

import router_rebooter_module # Defined in `pyscript_modules`

state.set("pyscript.router_rebooter_status", 
          "Ready", 
          new_attributes={
              "friendly_name": "Router Rebooter Status",
              "icon": "mdi:restart"
          })

state.set("pyscript.extender_rebooter_status", 
          "Ready", 
          new_attributes={
              "friendly_name": "Extender Rebooter Status",
              "icon": "mdi:restart"
          })

@service
def reboot_router():
    """Reboots the router."""
    pyscript.router_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering reboot"
    success, message = task.executor(router_rebooter_module.reboot_router)
    if success:
        pyscript.router_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Success!"
    else:
        pyscript.router_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {message[:50]}..."

@service
def reboot_extender():
    """Reboots the extender."""
    pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering reboot"
    success, message = task.executor(router_rebooter_module.reboot_extender)
    if success:
        pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Success!"
    else:
        pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {message[:50]}..."
