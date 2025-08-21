import sys
from datetime import datetime

# Add the pyscript_modules directory to Python's module search path (`compose.yaml` is configured to mount contents of `python_modules` into container automatically) 
# See https://hacs-pyscript.readthedocs.io/en/latest/reference.html#importing
if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")

import router_rebooter_module # Defined in `pyscript_modules`

# Make Extender Rebooter status persistent across HA restarts
# Initializes `pyscript.extender_rebooter_status` state variable (entity_id) if it doesn't exist
state.persist("pyscript.extender_rebooter_status", "Ready", {
    "friendly_name": "Extender Rebooter Status",
    "icon": "mdi:restart"
})

# Make Router Rebooter status persistent across HA restarts
# Initializes `pyscript.router_rebooter_status` state variable (entity_id) if it doesn't exist
state.persist("pyscript.router_rebooter_status", "Ready", {
    "friendly_name": "Router Rebooter Status",
    "icon": "mdi:restart"
})

@service
def reboot_router():
    """Reboots the router."""
    pyscript.router_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] Executing Reboot Command..."
    # Run blocking Selenium code from module with `task.executor()`
    success, message = task.executor(router_rebooter_module.reboot_router)
    if success:
        pyscript.router_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] Success!"
    else:
        pyscript.router_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] ERROR | Check Logs!"
        log.error(f"[Router Rebooter]: {message}")

@service
def reboot_extender():
    """Reboots the extender."""
    pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] Executing Reboot Command..."
    # Run blocking Selenium code from module with `task.executor()`
    success, message = task.executor(router_rebooter_module.reboot_extender)
    if success:
        pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] Success!"
    else:
        pyscript.extender_rebooter_status = f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] ERROR | Check Logs!"
        log.error(f"[Extender Rebooter]: {message}")
