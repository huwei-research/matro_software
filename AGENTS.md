# MATRO 软件交付仓库

本仓发布 MATRO 求解器和论文图表复现材料。[说明](README.md)给出安装方法，[当前交付](STATE.md)登记版本。开发主源为工作区 Research/matro，科研过程记录在研究主仓的 research_log.md。维护者在主源完成修改与核验后，同步已确定的交付内容。

软件接口位于 src/matro。运行 `python -m pytest tests` 检查公开接口，`python -m build` 构建安装包。实验数据和绘图入口见[复现说明](reproduction/README.md)。发布时核对交付清单中的 SHA-256。

<!-- project-ownership -->
```json
{"maintenance": "delivery", "project_id": "matro", "source_root": "Research/matro", "status": "aligned"}
```
<!-- /project-ownership -->
