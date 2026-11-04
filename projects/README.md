# Projects

Your local work goes here. This folder is ignored by Git; the example and template are the only tracked Blender artifacts.

Create a project with:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name my-ring
```

Each project contains:

```
projects\my-ring\
├─ README.md       ← the brief and next steps
├─ ring.blend      ← the working scene
├─ scripts\        ← every build/iteration script
└─ renders\        ← hero.png and previews
```

Open `projects\my-ring\ring.blend` in Blender, start OpenCode at the repository root, and paste a prompt. See [docs/04-first-project.md](../docs/04-first-project.md).
