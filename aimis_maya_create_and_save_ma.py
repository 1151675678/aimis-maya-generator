# Maya Python script: generate a simple low-poly fan character (original), create joints and skinCluster, and save as Maya ASCII (.ma)
# Run inside Maya Script Editor (Python)
import maya.cmds as cmds
import os
import traceback

def make_lambert(name, color):
    # create lambert and corresponding shadingGroup (reuse if exists)
    mat = name
    sg = name + "SG"
    if not cmds.objExists(mat):
        mat = cmds.shadingNode('lambert', asShader=True, name=name)
    if not cmds.objExists(sg):
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg)
    # connect if not connected
    try:
        if not cmds.isConnected(mat + ".outColor", sg + ".surfaceShader"):
            cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader", force=True)
    except:
        pass
    try:
        cmds.setAttr(mat + ".color", color[0], color[1], color[2], type="double3")
    except:
        pass
    return mat, sg

def create_scene_and_save_ascii():
    try:
        # new scene (overwrite current)
        cmds.file(new=True, force=True)

        # create materials and SGs
        torso_mat, torso_sg = make_lambert('TorsoMat', (0.18, 0.45, 0.75))
        skin_mat, skin_sg   = make_lambert('SkinMat', (0.98, 0.85, 0.72))
        hair_mat, hair_sg   = make_lambert('HairMat', (0.08, 0.22, 0.55))
        skirt_mat, skirt_sg = make_lambert('SkirtMat', (0.95, 0.70, 0.18))
        leg_mat, leg_sg     = make_lambert('LegMat', (0.12, 0.12, 0.12))

        meshes = []

        # Torso
        torso = cmds.polyCube(name='Torso', width=0.9, height=1.6, depth=0.56)[0]
        cmds.move(0, 0.8, 0, torso)
        cmds.sets(torso, e=True, forceElement=torso_sg)
        meshes.append(torso)

        # Head
        head = cmds.polySphere(name='Head', radius=0.35, subdivisionsX=20, subdivisionsY=12)[0]
        cmds.move(0, 2.1, 0, head)
        cmds.sets(head, e=True, forceElement=skin_sg)
        meshes.append(head)

        # Hair
        hair = cmds.polySphere(name='Hair', radius=0.38, subdivisionsX=18, subdivisionsY=10)[0]
        cmds.move(0, 2.15, -0.02, hair)
        cmds.scale(1.02, 0.92, 1.0, hair)
        cmds.sets(hair, e=True, forceElement=hair_sg)
        meshes.append(hair)

        # Left/Right Arms
        left_arm = cmds.polyCylinder(name='LeftArm', radius=0.12, height=1.05, subdivisionsX=12)[0]
        cmds.move(-0.62, 1.45, 0, left_arm)
        cmds.sets(left_arm, e=True, forceElement=skin_sg)
        meshes.append(left_arm)

        right_arm = cmds.polyCylinder(name='RightArm', radius=0.12, height=1.05, subdivisionsX=12)[0]
        cmds.move(0.62, 1.45, 0, right_arm)
        cmds.sets(right_arm, e=True, forceElement=skin_sg)
        meshes.append(right_arm)

        # Left/Right Legs
        left_leg = cmds.polyCylinder(name='LeftLeg', radius=0.135, height=1.1, subdivisionsX=12)[0]
        cmds.move(-0.18, 0.55, 0, left_leg)
        cmds.sets(left_leg, e=True, forceElement=leg_sg)
        meshes.append(left_leg)

        right_leg = cmds.polyCylinder(name='RightLeg', radius=0.135, height=1.1, subdivisionsX=12)[0]
        cmds.move(0.18, 0.55, 0, right_leg)
        cmds.sets(right_leg, e=True, forceElement=leg_sg)
        meshes.append(right_leg)

        # Skirt
        skirt = cmds.polyCylinder(name='Skirt', radius=0.62, height=0.38, subdivisionsX=20)[0]
        cmds.move(0, 0.95, 0, skirt)
        cmds.sets(skirt, e=True, forceElement=skirt_sg)
        meshes.append(skirt)

        # Soft edge shading
        for m in meshes:
            try:
                cmds.polySoftEdge(m, angle=180, ch=False)
            except:
                pass

        # Parent to Torso
        for m in meshes:
            if m != 'Torso':
                try:
                    cmds.parent(m, 'Torso')
                except:
                    pass

        # Create joints: Hips -> Spine1 -> Chest -> Head
        cmds.select(clear=True)
        hips = cmds.joint(name='Hips_joint', p=(0, 0.5, 0))
        spine1 = cmds.joint(name='Spine1_joint', p=(0, 1.1, 0))
        chest = cmds.joint(name='Chest_joint', p=(0, 1.6, 0))
        head_j = cmds.joint(name='Head_joint', p=(0, 2.1, 0))
        # Create limbs from hips
        cmds.select(hips)
        left_arm_j = cmds.joint(name='LeftArm_joint', p=(-0.6, 1.5, 0))
        cmds.select(hips)
        right_arm_j = cmds.joint(name='RightArm_joint', p=(0.6, 1.5, 0))
        cmds.select(hips)
        left_leg_j = cmds.joint(name='LeftLeg_joint', p=(-0.18, 0.0, 0))
        cmds.select(hips)
        right_leg_j = cmds.joint(name='RightLeg_joint', p=(0.18, 0.0, 0))

        cmds.select(clear=True)

        # Skin bind
        joint_list = ['Hips_joint','Spine1_joint','Chest_joint','Head_joint','LeftArm_joint','RightArm_joint','LeftLeg_joint','RightLeg_joint']
        to_bind = [name for name in ['Torso','Head','Hair','LeftArm','RightArm','LeftLeg','RightLeg','Skirt'] if cmds.objExists(name)]

        try:
            cmds.select(to_bind, r=True)
            cmds.select(joint_list, add=True)
            cmds.skinCluster(joint_list, to_bind, toSelectedBones=True, maximumInfluences=4, normalizeWeights=1, name='Body_skinCluster')
        except Exception:
            for mesh in to_bind:
                try:
                    cmds.select(mesh, r=True)
                    cmds.select(joint_list, add=True)
                    cmds.skinCluster(joint_list, mesh, toSelectedBones=True, maximumInfluences=4, normalizeWeights=1)
                except:
                    pass

        # Freeze transforms
        for m in to_bind:
            try:
                if cmds.objExists(m):
                    cmds.makeIdentity(m, apply=True, t=1, r=1, s=1, n=0)
            except:
                pass

        # Save as Maya ASCII to Desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        out_file = os.path.join(desktop, "aimis_fan_model_for_maya.ma")
        cmds.file(rename=out_file)
        cmds.file(save=True, type='mayaAscii')
        print("Saved Maya ASCII scene to:", out_file)

    except Exception as e:
        print("Error during creation:\n", e)
        traceback.print_exc()

if __name__ == "__main__":
    create_scene_and_save_ascii()
