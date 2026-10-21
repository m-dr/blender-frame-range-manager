bl_info = {
    "name": "Frame Range Manager",
    "author": "MD",
    "version": (0, 1, 1),
    "blender": (4, 0, 0),
    "location": "Timeline / Dope Sheet / Graph / NLA / Sequencer Headers > Frame Range Popover",
    "description": "Store, manage, edit, and restore named frame ranges shared across all scenes in a blendfile.",
    "category": "Animation",
}

import bpy


def sync_frame_ranges(source_scene):
    """Sync frame ranges from source_scene to all other scenes in the blendfile."""
    if not source_scene:
        return
    for scn in bpy.data.scenes:
        if scn == source_scene:
            continue
        scn.frame_ranges.clear()
        for item in source_scene.frame_ranges:
            new_item = scn.frame_ranges.add()
            new_item.skip_sync = True
            new_item.name = item.name
            new_item.frame_start = item.frame_start
            new_item.frame_end = item.frame_end
            new_item.use_preview_range = item.use_preview_range
            new_item.frame_preview_start = item.frame_preview_start
            new_item.frame_preview_end = item.frame_preview_end
            new_item.skip_sync = False
        scn.frame_range_active_index = source_scene.frame_range_active_index


def _on_property_update(self, context):
    """Callback triggered when preset properties (name, start, end) are edited inline."""
    if getattr(self, "skip_sync", False):
        return
    if context and hasattr(context, "scene") and context.scene:
        sync_frame_ranges(context.scene)


class FrameRangeItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        default="Range",
        description="Name of this frame range preset",
        update=_on_property_update
    )
    frame_start: bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        description="Start frame for this range",
        update=_on_property_update
    )
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        default=250,
        description="End frame for this range",
        update=_on_property_update
    )
    use_preview_range: bpy.props.BoolProperty(
        name="Use Preview Range",
        default=False,
        description="Whether preview range was active when saved",
        update=_on_property_update
    )
    frame_preview_start: bpy.props.IntProperty(
        name="Preview Start Frame",
        default=1,
        update=_on_property_update
    )
    frame_preview_end: bpy.props.IntProperty(
        name="Preview End Frame",
        default=250,
        update=_on_property_update
    )
    skip_sync: bpy.props.BoolProperty(default=False)


class SCENE_OT_frame_range_add(bpy.types.Operator):
    """Store the current scene frame range as a new named preset"""
    bl_idname = "scene.frame_range_add"
    bl_label = "Store Current Frame Range"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(
        name="Preset Name",
        default=""
    )

    def execute(self, context):
        scene = context.scene
        item = scene.frame_ranges.add()
        
        item.skip_sync = True
        if self.name:
            item.name = self.name
        else:
            item.name = f"Shot {len(scene.frame_ranges):02d}"
            
        if scene.use_preview_range:
            item.frame_start = scene.frame_preview_start
            item.frame_end = scene.frame_preview_end
        else:
            item.frame_start = scene.frame_start
            item.frame_end = scene.frame_end

        item.use_preview_range = scene.use_preview_range
        item.frame_preview_start = item.frame_start
        item.frame_preview_end = item.frame_end
        item.skip_sync = False
        
        scene.frame_range_active_index = len(scene.frame_ranges) - 1
        sync_frame_ranges(scene)
        
        mode_info = "preview " if scene.use_preview_range else ""
        self.report({'INFO'}, f"Saved {mode_info}frame range '{item.name}' ({item.frame_start}-{item.frame_end})")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class SCENE_OT_frame_range_apply(bpy.types.Operator):
    """Apply the selected frame range preset to the current scene"""
    bl_idname = "scene.frame_range_apply"
    bl_label = "Apply Frame Range"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Index", default=-1)

    def execute(self, context):
        scene = context.scene
        idx = self.index if self.index >= 0 else scene.frame_range_active_index
        
        if 0 <= idx < len(scene.frame_ranges):
            item = scene.frame_ranges[idx]
            
            if scene.use_preview_range:
                scene.frame_preview_start = item.frame_start
                scene.frame_preview_end = item.frame_end
                mode_info = "preview "
            else:
                scene.frame_start = item.frame_start
                scene.frame_end = item.frame_end
                mode_info = ""
                
            scene.frame_range_active_index = idx
            sync_frame_ranges(scene)
            
            self.report({'INFO'}, f"Applied {mode_info}frame range '{item.name}' ({item.frame_start}-{item.frame_end})")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Invalid frame range index")
            return {'CANCELLED'}


class SCENE_OT_frame_range_update(bpy.types.Operator):
    """Overwrite the selected frame range preset with current scene frames"""
    bl_idname = "scene.frame_range_update"
    bl_label = "Update Preset from Scene"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Index", default=-1)

    def execute(self, context):
        scene = context.scene
        idx = self.index if self.index >= 0 else scene.frame_range_active_index
        
        if 0 <= idx < len(scene.frame_ranges):
            item = scene.frame_ranges[idx]
            item.skip_sync = True
            if scene.use_preview_range:
                item.frame_start = scene.frame_preview_start
                item.frame_end = scene.frame_preview_end
            else:
                item.frame_start = scene.frame_start
                item.frame_end = scene.frame_end
            item.use_preview_range = scene.use_preview_range
            item.frame_preview_start = item.frame_start
            item.frame_preview_end = item.frame_end
            item.skip_sync = False
            
            sync_frame_ranges(scene)
            mode_info = "preview " if scene.use_preview_range else ""
            self.report({'INFO'}, f"Updated {mode_info}frame range '{item.name}' to ({item.frame_start}-{item.frame_end})")
            return {'FINISHED'}
        return {'CANCELLED'}


class SCENE_OT_frame_range_remove(bpy.types.Operator):
    """Remove a stored frame range preset"""
    bl_idname = "scene.frame_range_remove"
    bl_label = "Delete Preset"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Index", default=-1)

    def execute(self, context):
        scene = context.scene
        idx = self.index if self.index >= 0 else scene.frame_range_active_index
        
        if 0 <= idx < len(scene.frame_ranges):
            name = scene.frame_ranges[idx].name
            scene.frame_ranges.remove(idx)
            if scene.frame_range_active_index >= len(scene.frame_ranges):
                scene.frame_range_active_index = max(0, len(scene.frame_ranges) - 1)
            sync_frame_ranges(scene)
            self.report({'INFO'}, f"Removed frame range '{name}'")
            return {'FINISHED'}
        return {'CANCELLED'}


class TIME_PT_frame_ranges_popover(bpy.types.Panel):
    """Popover panel for Frame Ranges"""
    bl_label = "Stored Frame Ranges"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'HEADER'
    bl_idname = "TIME_PT_frame_ranges_popover"

    def draw(self, context):
        layout = self.layout
        # Compact initial width (starts reasonably short)
        layout.ui_units_x = 14
        
        scene = context.scene
        
        col = layout.column(align=True)
        col.operator("scene.frame_range_add", text="Store Current Range", icon='ADD')
        
        col.separator()
        
        if not scene.frame_ranges:
            box = col.box()
            box.label(text="No stored ranges yet", icon='INFO')
            return

        for idx, item in enumerate(scene.frame_ranges):
            is_active = (idx == scene.frame_range_active_index)
            box = col.box()
            
            # Row 1: Apply / Active Toggle + Full Preset Name
            r1 = box.row(align=True)
            apply_op = r1.operator(
                "scene.frame_range_apply",
                text="",
                icon='CHECKMARK' if is_active else 'PLAY'
            )
            apply_op.index = idx
            r1.prop(item, "name", text="")
            
            # Row 2: Compact Start, End, Update, and Delete
            r2 = box.row(align=True)
            r2.prop(item, "frame_start", text="S")
            r2.prop(item, "frame_end", text="E")
            
            upd_op = r2.operator("scene.frame_range_update", text="", icon='FILE_REFRESH')
            upd_op.index = idx
            
            del_op = r2.operator("scene.frame_range_remove", text="", icon='X')
            del_op.index = idx


def draw_timeline_header_button(self, context):
    layout = self.layout
    scene = context.scene
    
    # Active preset label for header button display
    active_idx = scene.frame_range_active_index
    label = ""
    if 0 <= active_idx < len(scene.frame_ranges):
        label = scene.frame_ranges[active_idx].name

    # Truncate header button text so long preset names don't stretch the popover popup container
    disp_text = ""
    if label:
        disp_text = label[:14] + "..." if len(label) > 14 else label

    layout.popover(
        panel="TIME_PT_frame_ranges_popover",
        text=disp_text if disp_text else "Ranges",
        icon='PRESET',
    )


classes = (
    FrameRangeItem,
    SCENE_OT_frame_range_add,
    SCENE_OT_frame_range_apply,
    SCENE_OT_frame_range_update,
    SCENE_OT_frame_range_remove,
    TIME_PT_frame_ranges_popover,
)


# Headers and Playback Control regions where timeline controls are displayed
HEADER_CLASSES = (
    "DOPESHEET_HT_header",
    "DOPESHEET_HT_playback_controls",
    "GRAPH_HT_header",
    "GRAPH_HT_playback_controls",
    "NLA_HT_header",
    "NLA_HT_playback_controls",
    "SEQUENCER_HT_header",
    "SEQUENCER_HT_playback_controls",
    "CLIP_HT_header",
    "TIME_HT_header",
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.frame_ranges = bpy.props.CollectionProperty(type=FrameRangeItem)
    bpy.types.Scene.frame_range_active_index = bpy.props.IntProperty(default=0)

    # Append to all timeline, playback, and animation headers
    for header_name in HEADER_CLASSES:
        header_cls = getattr(bpy.types, header_name, None)
        if header_cls and hasattr(header_cls, "append"):
            try:
                header_cls.append(draw_timeline_header_button)
            except Exception:
                pass


def unregister():
    # Remove from all timeline, playback, and animation headers
    for header_name in HEADER_CLASSES:
        header_cls = getattr(bpy.types, header_name, None)
        if header_cls and hasattr(header_cls, "remove"):
            try:
                header_cls.remove(draw_timeline_header_button)
            except Exception:
                pass

    if hasattr(bpy.types.Scene, "frame_ranges"):
        del bpy.types.Scene.frame_ranges
    if hasattr(bpy.types.Scene, "frame_range_active_index"):
        del bpy.types.Scene.frame_range_active_index

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass


if __name__ == "__main__":
    register()
