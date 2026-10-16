# Resource pack Evo Extract

Décors des menus DeluxeMenus du serveur (Minecraft 26.2, format 88).

- `EvoExtract-pack.zip` : le pack proposé aux joueurs (lien dans `server.properties`).
- `pack/` : contenu du pack (polices et images).
- `src/` : scripts qui dessinent les décors (`draw.py`) et construisent le pack (`build_pack.py`).
- `src/hud.py` : icônes et filets dorés de la tablist et du scoreboard (glyphes U+E200 et suivants).
- `src/items/` : objets 3D (armes de classe, matériaux de raid, sacoches) du namespace `evo`. `python3 src/items/generate.py` régénère `pack/assets/evo/{items,models/item,textures/item}` et l'aperçu `src/items/apercu.png`. Les objets utilisent le composant `item_model` (`evo:<id>`), sans `custom_model_data` ni surcharge des objets vanilla.
