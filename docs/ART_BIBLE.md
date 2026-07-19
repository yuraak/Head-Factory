# PolyHeads Art Bible

Version 1.0

## Purpose

PolyHeads is a library of floating portrait heads that appear to have been produced by one art team, in one engine, for one unreleased 2002 console title. The collection is not fan art and does not imitate promotional photography. Every subject is rebuilt through the same technical and visual language.

## Immutable output rules

- Canvas: 2048 × 1152, 16:9
- Format: PNG with true transparent alpha
- Exactly one centered head
- Head silhouette occupies 84–88% of canvas height
- Front view: pitch 0°, yaw 0°, roll 0°
- No neck, shoulders, torso, collar, clothing, hands, body, pedestal, text, logo, border, shadow, environment, gradient, vignette, smoke, or effects

## Camera and composition

The camera and framing never change. Use an orthographic feel or extremely weak perspective. The subject looks directly at the camera. The visible silhouette is centered on the true canvas center. No dynamic pose, crop variation, or asymmetry is introduced for style.

## Geometry

- Approximate budget: 1,500–3,500 triangles
- Hard faceted geometry
- Visible polygon structure
- No subdivision smoothing
- Large cheek planes
- Angular jaw and nose bridge
- Simplified eyelids, lips, and ears

Consistency applies to topology language and polygon density, not identical anatomy. Each subject must preserve their own cranial silhouette, age, facial proportions, and distinctive structure.

## Textures and materials

- Diffuse-only appearance
- Texture density resembling 256–512 px console textures
- Slight pixelation is desirable
- Matte console-era materials
- No PBR, normal maps, roughness maps, metallic maps, AO, subsurface scattering, pores, or microdetail

## Hair

Hair is chunky solid geometry. No realistic strands, groom systems, wisps, or alpha-card hair. Hair silhouette must remain identity-specific.

## Lighting

- One frontal key light slightly above eye level
- One very subtle frontal fill
- Strong, simple console-era contrast
- No rim light, bloom, glow, GI, cinematic grading, dramatic color wash, or environment lighting

## Identity preservation

Before rendering, identify four to six unmistakable markers for the subject. These may include:

- cranial and facial silhouette
- hairstyle or hairline
- age and skin structure
- mask, glasses, headgear, makeup, scars, or piercings
- eye shape, nose, jaw, mouth, facial hair, or distinctive proportions

Do not reuse a generic handsome face, long-haired male template, fixed jaw, fixed nose, fixed smile, or one recurring anatomy. The pipeline remains fixed; identity does not.

## Accessories

Only accessories inseparable from the identity are allowed. Examples include Neo’s glasses, Naruto’s headband, a defining mask, or iconic headgear. Decorative clothing and unrelated objects are forbidden.

## Quality control

Reject the asset when any of the following is true:

- duplicate subject
- resembles a previous subject more than the intended identity
- generic recurring face template
- visible neck, shoulders, clothing, or body
- incorrect framing or head scale
- non-transparent background or fake checkerboard transparency
- gray, blurred, gradient, vignette, halo, shadow, or backdrop
- modern PBR, photorealistic, painterly, or outlined illustration style
- incorrect angle or head tilt
- text, logo, border, watermark, or extra object
- more than one portrait

## Collection principle

When hundreds of approved portraits are shown together, they must look as though they were modeled, textured, lit, and exported by the same team and engine. The only intentional variable is the identity of the subject.
