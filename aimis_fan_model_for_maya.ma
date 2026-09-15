//Maya ASCII 2024 scene
//Created by aimis-maya-generator
//This file creates simple low-poly geometry and joints. It may require adjustments in Maya.

currentUnit -l centimeter -a degree -t film;
// Create geometry
polyCube -w 0.9 -h 1.6 -d 0.56 -name "Torso";
move -r 0 0.8 0 Torso;
polySphere -r 0.35 -name "Head";
move -r 0 2.1 0 Head;
polySphere -r 0.38 -name "Hair";
move -r 0 2.15 -0.02 Hair;
scale -r 1.02 0.92 1 Hair;
polyCylinder -r 0.12 -h 1.05 -name "LeftArm";
move -r -0.62 1.45 0 LeftArm;
polyCylinder -r 0.12 -h 1.05 -name "RightArm";
move -r 0.62 1.45 0 RightArm;
polyCylinder -r 0.135 -h 1.1 -name "LeftLeg";
move -r -0.18 0.55 0 LeftLeg;
polyCylinder -r 0.135 -h 1.1 -name "RightLeg";
move -r 0.18 0.55 0 RightLeg;
polyCylinder -r 0.62 -h 0.38 -name "Skirt";
move -r 0 0.95 0 Skirt;

// Create joints
select -cl;
joint -p 0 0.5 0 -name "Hips_joint";
joint -p 0 1.1 0 -name "Spine1_joint";
joint -p 0 1.6 0 -name "Chest_joint";
joint -p 0 2.1 0 -name "Head_joint";
select -cl;
select -r Hips_joint;
joint -p -0.6 1.5 0 -name "LeftArm_joint";
select -r Hips_joint;
joint -p 0.6 1.5 0 -name "RightArm_joint";
select -r Hips_joint;
joint -p -0.18 0.0 0 -name "LeftLeg_joint";
select -r Hips_joint;
joint -p 0.18 0.0 0 -name "RightLeg_joint";
select -cl;

// Bind skinCluster (attempt)
select -r Torso Head Hair LeftArm RightArm LeftLeg RightLeg Skirt;
select -add Hips_joint Spine1_joint Chest_joint Head_joint LeftArm_joint RightArm_joint LeftLeg_joint RightLeg_joint;
try
{
    skinCluster -tsb Hips_joint Spine1_joint Chest_joint Head_joint LeftArm_joint RightArm_joint LeftLeg_joint RightLeg_joint Torso Head Hair LeftArm RightArm LeftLeg RightLeg Skirt -name "Body_skinCluster";
}
catch ($e)
{
    // skinCluster creation may fail in some Maya versions; please bind manually if needed
}

// Freeze transforms
makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 Torso Head Hair LeftArm RightArm LeftLeg RightLeg Skirt;

print "Finished creating basic scene.\n";
