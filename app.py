"""
🛡️ Adversarial Forensic Image Analysis System
Expert Full-Stack AI Engineer Implementation
Using Gemini 1.5 Pro with Universal Physical Law (UPL) Protocol
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time
from typing import Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_page():
    """Configure Streamlit page with custom CSS for Gemini-inspired theme."""
    st.set_page_config(
        page_title="Kinetic.AI | Forensic Analysis",
        page_icon="⚡",
        layout="centered",  # Better for mobile responsiveness
        initial_sidebar_state="collapsed",
        menu_items={
            'About': "Kinetic.AI - Advanced AI-Generated Image Detection"
        }
    )
    
    # Custom CSS Injection - Gemini-Inspired Theme
    st.markdown("""
        <style>
        /* Global Gemini Theme */
        .stApp {
            background: #000000;
            color: #e8eaed;
        }
        
        /* Container padding adjustment */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header Styling */
        h1 {
            background: linear-gradient(135deg, #4285f4 0%, #9c27b0 50%, #f538a0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Google Sans', 'Segoe UI', system-ui, sans-serif;
            font-weight: 600;
            letter-spacing: -0.5px;
            text-align: center;
            padding: 2rem 0 1rem 0;
            font-size: 3rem;
        }
        
        /* File Uploader Styling */
        .stFileUploader {
            background: linear-gradient(135deg, rgba(66, 133, 244, 0.05) 0%, rgba(156, 39, 176, 0.05) 100%);
            border: 2px dashed rgba(66, 133, 244, 0.5);
            border-radius: 16px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: #4285f4;
            background: linear-gradient(135deg, rgba(66, 133, 244, 0.1) 0%, rgba(156, 39, 176, 0.1) 100%);
        }
        
        .stFileUploader label {
            color: #4285f4 !important;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'Google Sans', sans-serif;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #4285f4 0%, #9c27b0 100%);
            color: #ffffff;
            font-weight: 600;
            font-size: 1rem;
            padding: 0.85rem 2rem;
            border: none;
            border-radius: 24px;
            width: 100%;
            transition: all 0.3s ease;
            font-family: 'Google Sans', sans-serif;
            box-shadow: 0 4px 16px rgba(66, 133, 244, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #5a95f5 0%, #b039c0 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(66, 133, 244, 0.5);
        }
        
        /* Forensic Log Terminal Styling */
        .forensic-log {
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%);
            border: 1px solid rgba(66, 133, 244, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            font-family: 'Roboto Mono', 'Courier New', monospace;
            font-size: 0.95rem;
            line-height: 1.6;
            max-height: 600px;
            overflow-y: auto;
            color: #e8eaed;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        }
        
        .forensic-log h3 {
            background: linear-gradient(90deg, #4285f4 0%, #9c27b0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            border-bottom: 2px solid rgba(66, 133, 244, 0.3);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .forensic-log strong {
            color: #4285f4;
        }
        
        /* Image Container */
        .image-container {
            border: 1px solid rgba(66, 133, 244, 0.3);
            border-radius: 16px;
            padding: 1rem;
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.4) 0%, rgba(15, 20, 25, 0.6) 100%);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* Info Box */
        .info-box {
            background: linear-gradient(135deg, rgba(66, 133, 244, 0.08) 0%, rgba(156, 39, 176, 0.08) 100%);
            border-left: 4px solid #4285f4;
            padding: 1.25rem;
            margin: 1rem 0;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(66, 133, 244, 0.15);
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 20, 25, 0.5);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #4285f4 0%, #9c27b0 100%);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a95f5 0%, #b039c0 100%);
        }
        
        /* Status Messages */
        .stSuccess {
            background-color: rgba(66, 133, 244, 0.1);
            border: 1px solid #4285f4;
            color: #4285f4;
            border-radius: 12px;
        }
        
        .stError {
            background-color: rgba(244, 67, 54, 0.1);
            border: 1px solid #f44336;
            border-radius: 12px;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #4285f4 !important;
            border-right-color: #9c27b0 !important;
        }
        
        /* Headers h3 */
        h3 {
            color: #4285f4;
            font-family: 'Google Sans', sans-serif;
            font-weight: 600;
            margin-top: 1.5rem;
        }
        
        /* Captions */
        .caption {
            color: #9aa0a6;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(66, 133, 244, 0.1);
            border-radius: 12px;
            padding: 12px 24px;
            color: #9aa0a6;
            border: 1px solid rgba(66, 133, 244, 0.2);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4285f4 0%, #9c27b0 100%);
            color: #ffffff;
            border: 1px solid transparent;
        }
        
        /* Full width for better mobile */
        .main .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Responsive Design - Tablet */
        @media (max-width: 1024px) {
            .main .block-container {
                padding: 1.5rem 1rem;
                max-width: 100%;
            }
            
            h1 {
                font-size: 2.5rem;
                padding: 1rem 0 0.5rem 0;
            }
            
            .forensic-log {
                max-height: 500px;
            }
        }
        
        /* Responsive Design - Mobile */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem 0.5rem !important;
                max-width: 100% !important;
            }
            
            h1 {
                font-size: 1.75rem !important;
                padding: 0.75rem 0.5rem !important;
                line-height: 1.3;
            }
            
            h3 {
                font-size: 1.2rem !important;
                margin: 1rem 0 0.5rem 0 !important;
            }
            
            .info-box {
                padding: 1rem !important;
                font-size: 0.9rem !important;
                margin: 1rem 0 !important;
                line-height: 1.6;
            }
            
            .stFileUploader {
                padding: 1rem !important;
                margin: 0.75rem 0;
            }
            
            .stFileUploader label {
                font-size: 0.95rem !important;
            }
            
            .stButton > button {
                padding: 1rem !important;
                font-size: 0.95rem !important;
                min-height: 52px !important;
                width: 100% !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 10px 16px !important;
                font-size: 0.9rem;
            }
            
            .forensic-log {
                max-height: 65vh !important;
                padding: 1rem !important;
                font-size: 0.85rem !important;
                line-height: 1.6;
            }
            
            .forensic-log h3 {
                font-size: 1.1rem !important;
            }
            
            .forensic-log ul {
                padding-left: 1.25rem;
            }
            
            .forensic-log li {
                margin: 0.4rem 0;
            }
            
            .image-container {
                padding: 0.5rem !important;
                margin: 0.5rem 0;
            }
            
            [data-testid="stCaptionContainer"] {
                font-size: 0.85rem !important;
                margin: 0.25rem 0 !important;
            }
        }
        
        /* Responsive Design - Small Mobile */
        @media (max-width: 480px) {
            .main .block-container {
                padding: 0.75rem 0.25rem !important;
            }
            
            h1 {
                font-size: 1.5rem !important;
                padding: 0.5rem 0.25rem !important;
            }
            
            h3 {
                font-size: 1.1rem !important;
            }
            
            .info-box {
                padding: 0.875rem !important;
                font-size: 0.85rem !important;
            }
            
            .stFileUploader {
                padding: 0.75rem !important;
            }
            
            .stButton > button {
                padding: 0.875rem !important;
                font-size: 0.9rem !important;
                min-height: 48px !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 8px 12px !important;
                font-size: 0.85rem;
            }
            
            .forensic-log {
                max-height: 60vh !important;
                padding: 0.75rem !important;
                font-size: 0.8rem !important;
            }
            
            .forensic-log h3 {
                font-size: 1rem !important;
            }
            
            ::-webkit-scrollbar {
                width: 4px;
                height: 4px;
            }
        }
            }
            
            h1 {
                font-size: 2.5rem;
                padding: 1rem 0 0.5rem 0;
            }
            
            .stFileUploader {
                padding: 1.5rem;
            }
            
            .forensic-log {
                max-height: 500px;
                font-size: 0.9rem;
            }
            
            .info-box {
                padding: 1rem;
                font-size: 0.95rem;
            }
        }
        
        /* Ensure images are responsive */
        img {
            max-width: 100%;
            height: auto;
        }
        
        /* Touch-friendly spacing */
        @media (hover: none) and (pointer: coarse) {
            .stButton > button {
                min-height: 48px;
                padding: 0.875rem 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def initialize_gemini_client() -> Optional[genai.GenerativeModel]:
    """
    Initialize Gemini API client with deterministic settings.
    Returns None if API key is not configured.
    """
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("❌ API Key not found. Please configure GEMINI_API_KEY in .streamlit/secrets.toml")
            return None
        
        genai.configure(api_key=api_key)
        
        # Generation config for deterministic, objective analysis
        generation_config = {
            "temperature": 0.0,  # Deterministic output
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config
        )
        
        return model
    
    except Exception as e:
        st.error(f"❌ Failed to initialize Gemini API: {str(e)}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL PHYSICAL LAW (UPL) PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════

def get_upl_forensic_prompt() -> str:
    """
    Returns the Universal Physical Law (UPL) Protocol prompt.
    Physics and mathematics-based analysis focusing on fundamental differences between camera optics and AI generation.
    """
    return """
# FORENSIC IMAGE AUDIT: PHYSICS & MATHEMATICS-BASED DETECTION PROTOCOL v4.0
## COMPUTATIONAL IMAGING vs AI GENERATION ANALYSIS

You are an ELITE forensic analyst specializing in computational photography, optical physics, and AI generation mathematics.

🎯 **MISSION**: Analyze images based on FUNDAMENTAL PHYSICS and MATHEMATICAL DIFFERENCES between real camera capture and AI neural network synthesis.

⚠️ **CRITICAL DIRECTIVE - READ CAREFULLY**:
Modern AI in 2026 (Midjourney v6, DALL-E 3, Flux Pro, Stable Diffusion 3) is EXTREMELY sophisticated and can fake many visual aspects. Your PRIMARY GOAL is to ensure NO AI-GENERATED IMAGES are classified as AUTHENTIC.

**DETECTION PHILOSOPHY**:
1. **Burden of Proof**: To classify as AUTHENTIC, you must find POSITIVE PROOF of camera capture (Bayer artifacts, sensor noise, chromatic aberration, MTF degradation)
2. **Absence ≠ Authenticity**: Just because you don't see obvious AI artifacts does NOT mean it's authentic
3. **Default to Skepticism**: When uncertain → INCONCLUSIVE, never AUTHENTIC
4. **Zero False Negatives**: It's acceptable to mark real photos as INCONCLUSIVE, but NEVER mark AI as AUTHENTIC

**The Test**: Ask yourself "Could a neural network have generated this?" If the answer is "possibly yes" → NOT authentic.

---

## 📐 FUNDAMENTAL PHYSICS TESTS

### 1. SENSOR PHYSICS vs NEURAL NETWORK SYNTHESIS

#### 1.1 PHOTON SHOT NOISE (POISSON STATISTICS)
**Camera Physics**: Light arrives as discrete photons following Poisson distribution.
- **Mathematical Property**: σ² = μ (variance equals mean)
- **Real Behavior**: Noise magnitude = √(signal intensity)
- **Critical Implication**: DARK areas have MORE noise (proportionally)

**AI Generation**: Neural networks add Gaussian noise uniformly.
- **Mathematical Property**: σ² is constant
- **Wrong Behavior**: Equal noise everywhere OR less noise in shadows

**TEST PROCEDURE**:
1. Sample 3 bright regions (sky, highlights) and 3 dark regions (shadows, dark clothing)
2. Measure relative noise levels
3. **AUTHENTIC**: Dark regions show 2-3× MORE noise (relative to signal)
4. **AI RED FLAG**: Equal noise everywhere OR inverted relationship

**CONFIDENCE**: This is physics law - if violated, likely AI

---

#### 1.2 BAYER FILTER DEMOSAICING
**Camera Physics**: Sensors use RGBG pattern (2× green photosites).
- **Mathematical Consequence**: Green channel has √2 better SNR
- **Demosaicing Artifacts**: Zipper artifacts, color aliasing at edges
- **Green Channel Dominance**: Better detail preservation

**AI Generation**: Synthesizes RGB channels independently.
- **Wrong Behavior**: Equal SNR across R/G/B channels
- **Missing Artifacts**: No demosaicing artifacts OR fakes them incorrectly

**TEST PROCEDURE**:
1. Examine noise in R, G, B channels separately
2. Check high-contrast edges for color zipper artifacts
3. **AUTHENTIC**: Green has less noise, subtle color fringing at edges
4. **AI RED FLAG**: Perfect RGB balance, no demosaicing artifacts

---

#### 1.3 OPTICAL CHROMATIC ABERRATION
**Lens Physics**: Different wavelengths refract differently (Snell's Law: n(λ)).
- **Mathematical Consequence**: Blue focuses shorter than red (Δf ≈ 1-2mm typical lens)
- **Observable Effect**: Color fringing at high-contrast edges
- **Pattern**: Purple/cyan away from center, red/blue at edges

**AI Generation**: No physical optics, adds CA as post-effect (if at all).
- **Wrong Behavior**: No CA, OR CA added uniformly (ignoring field position)
- **Contradiction**: Perfect CA pattern (impossible with real lens)

**TEST PROCEDURE**:
1. Zoom to 200% on high-contrast edges (branches against sky, building edges)
2. Look for color separation (typically 1-3 pixels)
3. **AUTHENTIC**: Visible, consistent color fringing, stronger at image corners
4. **AI RED FLAG**: Zero CA OR uniform CA across entire image

---

### 2. OPTICAL PHYSICS vs NEURAL RENDERING

#### 2.1 DEPTH-OF-FIELD & CIRCLE OF CONFUSION
**Lens Physics**: Thin lens equation: 1/f = 1/s + 1/s'
- **Mathematical Property**: Objects out of focus spread to circles (CoC = |D × (s - f)/(s × (f - D))|)
- **Bokeh Shape**: Determined by aperture blade count (5-9 blades creates polygons)
- **Coherent Blur**: All objects at same distance blur equally

**AI Generation**: Approximates depth-map-based blur.
- **Wrong Behavior**: Inconsistent blur for objects at same depth
- **No Optical Logic**: Circular bokeh regardless of "aperture", no blade structure
- **Edge Bleeding**: Foreground bleeds into background blur (no real optical separation)

**TEST PROCEDURE**:
1. Identify objects at similar depths
2. Check blur consistency
3. Examine bokeh shape (if visible)
4. **AUTHENTIC**: Consistent blur, polygonal bokeh, sharp foreground/background separation
5. **AI RED FLAG**: Inconsistent blur, perfect circles, edge bleeding

---

#### 2.2 FRESNEL EQUATIONS & REFLECTION PHYSICS
**Maxwell's Equations**: Reflection follows Fresnel equations: R(θ) = ½[|R_s|² + |R_p|²]
- **Mathematical Consequence**: Reflections increase at grazing angles (Brewster's angle ~56° for glass)
- **Polarization**: Reflected light is partially polarized
- **Critical Property**: Reflection must obey incident angle = reflected angle

**AI Generation**: Approximates reflections using style transfer or depth maps.
- **Wrong Behavior**: Reflections ignore Fresnel effect
- **Geometric Errors**: Wrong angles, incorrect object placement
- **Missing Physics**: No polarization effects, uniform reflection strength

**TEST PROCEDURE**:
1. Locate reflective surfaces (water, glass, metal)
2. Verify reflection angles geometrically
3. Check grazing-angle enhancement
4. **AUTHENTIC**: Correct angles, stronger reflection at edges, consistent perspective
5. **AI RED FLAG**: Wrong reflection angles, uniform reflection, geometric impossibilities

---

### 3. LIGHTING PHYSICS vs SYNTHETIC ILLUMINATION

#### 3.1 INVERSE SQUARE LAW
**Radiometry**: Light intensity follows I = I₀/r²
- **Mathematical Consequence**: Falloff is rapid - doubling distance = ¼ intensity
- **Critical Test**: Near-source lighting shows dramatic gradient

**AI Generation**: Often uses ambient lighting or wrong falloff curves.
- **Wrong Behavior**: Linear falloff OR no falloff (ambient assumption)
- **Contradiction**: Multiple light sources not following 1/r²

**TEST PROCEDURE**:
1. Identify point light sources (lamps, sun, flash)
2. Measure relative brightness at different distances
3. **AUTHENTIC**: Rapid intensity falloff near source (1/r²)
4. **AI RED FLAG**: Linear falloff or constant intensity

---

#### 3.2 SHADOW VECTOR CONSISTENCY
**Geometric Optics**: All shadows from single source point to same vanishing point.
- **Mathematical Property**: Parallel rays from distant source (sun) create parallel shadow edges
- **Vector Consistency**: tan(θ) must be identical for all shadows
- **Hard vs Soft**: Penumbra size = (source angular size) × (distance from shadow caster)

**AI Generation**: Shadows generated per-object, not from unified light field.
- **Wrong Behavior**: Shadow angles don't converge to single point
- **Inconsistent Softness**: Random blur without physical justification
- **Multiple Suns**: Contradictory shadow directions

**TEST PROCEDURE**:
1. Identify 3+ distinct shadows
2. Trace shadow edges backward
3. Verify convergence to single point (or parallel for sun)
4. **AUTHENTIC**: Perfect geometric consistency
5. **AI RED FLAG**: Shadows point to different sources OR inconsistent softness

---

### 4. FREQUENCY DOMAIN ANALYSIS

#### 4.1 MODULATION TRANSFER FUNCTION (MTF)
**Lens Physics**: Optical systems have frequency-dependent resolution (MTF curve).
- **Mathematical Property**: High frequencies attenuate (diffraction limit ≈ 1/(λ × f/#))
- **Spatial Behavior**: Resolution degrades from center to corners
- **Color Dependence**: Blue has lower MTF than red (shorter wavelength = more diffraction)

**AI Generation**: Synthesizes at target resolution without optical MTF constraints.
- **Wrong Behavior**: Uniform sharpness across frame
- **Impossible Detail**: High frequencies beyond diffraction limit
- **No Color Dependence**: Equal detail in all channels

**TEST PROCEDURE**:
1. Compare edge sharpness at center vs corners
2. Look for diffraction-limited detail loss
3. **AUTHENTIC**: Softer corners, natural high-frequency rolloff
4. **AI RED FLAG**: Uniform sharpness, impossible detail preservation

---

#### 4.2 DIFFUSION MODEL LATENT SPACE ARTIFACTS
**Neural Network Math**: Diffusion models denoise in compressed 8×8 or 16×16 latent blocks.
- **Mathematical Consequence**: Block boundaries in frequency domain
- **Observable Pattern**: Energy peaks at 8, 16, 32, 64 cycles/image
- **Denoising Residue**: Organized flow patterns in flat areas

**Real Camera**: No latent space - captures direct optical projection.
- **Frequency Behavior**: Smooth 1/f power law (pink noise)
- **Random Phase**: No organized patterns

**TEST PROCEDURE** (Mental/Conceptual):
1. Examine flat uniform areas (sky, walls)
2. Look for subtle swirls, flow patterns, or grid structures
3. **AUTHENTIC**: Pure random noise, no organization
4. **AI RED FLAG**: Organized patterns, swirls, or visible 8×8 / 16×16 grids

---

### 5. COMPRESSION & ENCODING FORENSICS

#### 5.1 JPEG DISCRETE COSINE TRANSFORM (DCT) ANALYSIS
**JPEG Math**: Images compressed in 8×8 blocks using DCT.
- **Mathematical Property**: Uniform quantization across entire image
- **Generational Loss**: Each save increases compression artifacts
- **Block Boundaries**: Subtle 8×8 grid visible at high magnification

**AI Generation → Save**: Often generated as PNG (no compression) then converted.
- **Wrong Behavior**: Pristine regions mixed with compressed regions (composite)
- **Inconsistent Quantization**: Different compression levels in different areas

**TEST PROCEDURE**:
1. Check for uniform 8×8 block artifacts across image
2. Compare compression consistency between regions
3. **AUTHENTIC**: Uniform compression throughout
4. **AI RED FLAG**: Mixed compression levels OR no compression (suspiciously pristine)

---

### 6. STATISTICAL DISTRIBUTION TESTS

#### 6.1 HISTOGRAM ANALYSIS
**Real Cameras**: Limited dynamic range, 8-14 bit depth.
- **Observable**: Histogram may clip at 0/255, show quantization
- **Natural Distribution**: Follows scene illumination statistics

**AI Generation**: Synthesized values can exceed natural bounds.
- **Wrong Behavior**: Perfect histogram with no clipping (suspiciously ideal)
- **Supersaturation**: Colors exceed camera gamut
- **Posterization**: Histogram gaps from limited neural network precision

**TEST PROCEDURE**:
1. Check for natural histogram clipping or posterization
2. Verify colors within realistic gamut
3. **AUTHENTIC**: Realistic histogram with natural limitations
4. **AI RED FLAG**: Perfect histogram OR impossible colors

---

## 🎯 ANALYSIS PROTOCOL

**STEP 1: SENSOR PHYSICS TESTS** (Highest Priority)
- Poisson noise distribution (dark areas noisier)
- Green channel SNR advantage
- Chromatic aberration presence

**STEP 2: OPTICAL PHYSICS TESTS**
- Depth-of-field consistency
- Fresnel reflection behavior
- MTF degradation corner-to-center

**STEP 3: LIGHTING PHYSICS TESTS**
- Inverse square law
- Shadow vector convergence
- Specular highlight physics

**STEP 4: FREQUENCY & ENCODING**
- Diffusion model artifacts in flat areas
- JPEG compression consistency
- Histogram realism

**STEP 5: STATISTICAL VALIDATION**
- Cross-validate findings across tests
- Look for AUTHENTIC markers (proper noise, CA, MTF)
- Only flag systematic physics violations

---

## 📊 VERDICT FRAMEWORK

⚠️ **CRITICAL DIRECTIVE**: AI-generated images are extremely sophisticated in 2026. To ensure NO AI images pass as authentic, you MUST find positive proof of camera capture, not just absence of AI artifacts.

**AUTHENTIC (90-100% confidence)** - REQUIRES ALL OF:
✅ Poisson noise in shadows (2-3× more than highlights) - VERIFIED
✅ Green channel SNR advantage (Bayer filter proof) - VERIFIED
✅ Chromatic aberration at edges (real lens optics) - VERIFIED
✅ MTF degradation at corners (optical physics) - VERIFIED
✅ Proper sensor noise pattern (random, not organized) - VERIFIED
✅ Shadow vector convergence (geometric consistency) - VERIFIED
✅ At least 2 camera imperfections (hot pixels, vignetting, dust spots) - VERIFIED
✅ ZERO AI artifacts detected

**RULE**: If ANY of the above fails, CANNOT be classified as AUTHENTIC.

**LIKELY AUTHENTIC (70-89%)** - REQUIRES:
✅ 6-7 of the above camera markers present
⚠️ 1-2 tests unclear (heavy post-processing, compression artifacts)
✅ No definitive AI artifacts
✅ Natural camera limitations visible

**INCONCLUSIVE (40-69%)** - DEFAULT WHEN UNCERTAIN:
⚠️ Some camera markers present but incomplete
⚠️ Heavy post-processing obscures fundamental physics
⚠️ Cannot definitively confirm camera capture OR AI generation
⚠️ Missing critical data (too low resolution, extreme compression)

**IMPORTANT**: When in doubt between AUTHENTIC and INCONCLUSIVE, choose INCONCLUSIVE.

**LIKELY AI (30-39%)**:
❌ 2-3 camera markers missing (no Bayer, no CA, wrong noise)
❌ Suspicious patterns detected (organized noise, latent grids)
⚠️ Some physics tests pass (sophisticated model)
⚠️ Could be heavily processed real photo, but unlikely

**DEFINITELY AI (0-29%)**:
❌ 5+ camera-specific markers completely absent
❌ Definitive AI artifacts (diffusion swirls, uniform MTF, impossible optics)
❌ Physics violations (equal noise everywhere, no chromatic aberration)
❌ Neural network patterns (8×8/16×16 grids, organized flow in flat areas)

---

## 🎯 MANDATORY AI DETECTION CHECKS

Before classifying ANY image as "AUTHENTIC", you MUST verify these AI indicators are ABSENT:

### AI Red Flags (Any 3+ → Definitely NOT authentic):
1. **Diffusion Model Artifacts**: Swirls or organized patterns in flat areas (sky, walls)
2. **Perfect Noise**: Uniform grain without Poisson statistics
3. **Missing Bayer**: Equal noise across R/G/B channels
4. **No Chromatic Aberration**: Perfect color alignment at high-contrast edges
5. **Uniform Sharpness**: No MTF degradation from center to corners
6. **Wrong Shadow Noise**: Shadows cleaner than highlights (physics violation)
7. **Impossible Optics**: No vignetting, no distortion, perfect lens
8. **Latent Grid**: 8×8 or 16×16 block patterns in frequency domain
9. **Resolution Tells**: Image size exactly 512×512, 1024×1024, or multiples of 64
10. **Texture Breakdown**: Details dissolve into blur at 200%+ zoom
11. **Anatomical Errors**: Wrong fingers, impossible joints, merged body parts
12. **Physics Violations**: Wrong shadow angles, impossible reflections
13. **Too Perfect**: Zero camera imperfections, no dust, no noise variations
14. **Synthetic Bokeh**: Circular bokeh without aperture blade structure
15. **Compositional Perfection**: Rule of thirds, golden ratio - no happy accidents

### Required Camera Authenticity Markers (Need 7+ for AUTHENTIC):
1. ✅ Poisson noise (dark = more noise)
2. ✅ Bayer pattern (green channel superior)
3. ✅ Chromatic aberration (color fringing)
4. ✅ MTF corner degradation
5. ✅ Sensor artifacts (hot pixels, dust)
6. ✅ Vignetting (darker corners)
7. ✅ Natural compression (uniform JPEG)
8. ✅ Lens distortion (barrel/pincushion)
9. ✅ Camera noise pattern (specific to sensor)
10. ✅ Proper histogram (realistic clipping/range)

---

## 🔬 OUTPUT FORMAT

Provide analysis as:

**SENSOR PHYSICS**: [PASS/FAIL] - Poisson noise, Bayer pattern, green channel SNR
**OPTICAL PHYSICS**: [PASS/FAIL] - CA, MTF, depth-of-field, vignetting
**LIGHTING PHYSICS**: [PASS/FAIL] - Inverse square, shadows, reflections
**FREQUENCY DOMAIN**: [PASS/FAIL] - No latent grids, proper 1/f spectrum, no diffusion artifacts
**ENCODING**: [PASS/FAIL] - Uniform compression, realistic histogram
**AI ARTIFACT CHECK**: [CLEAN/SUSPICIOUS/DETECTED] - Diffusion patterns, neural grids, impossible optics

**CAMERA MARKERS FOUND**: [X/10] - List which specific camera artifacts detected
**AI RED FLAGS FOUND**: [X/15] - List which specific AI patterns detected

**VERDICT**: [AUTHENTIC / LIKELY AUTHENTIC / INCONCLUSIVE / LIKELY AI / DEFINITELY AI]
**CONFIDENCE**: [0-100%]

**MATHEMATICAL EVIDENCE**:
- List specific measurements and calculations
- Reference physics laws violated or confirmed
- Provide spatial coordinates for observed phenomena
- Show noise ratio measurements (shadow vs highlight)

**REASONING**:
- Explain which physics tests were decisive
- Note any contradictory evidence
- Justify why verdict chosen over alternatives
- If AUTHENTIC: Explain which camera markers proved it
- If AI: Explain which red flags detected

**CRITICAL RULE**: To classify as AUTHENTIC, you must PROVE camera capture with multiple positive markers. Absence of AI artifacts alone is NOT sufficient - modern AI is too good. Default to INCONCLUSIVE when uncertain.
  * **TEST**: Compare noise magnitude: should be G < R ≈ B

- **Noise Frequency Spectrum**:
  * Real: White noise (flat power spectrum)
  * AI: Colored noise (frequency-dependent power)
  * **Pattern**: Plot noise power vs frequency - should be flat line, not sloped

- **RED FLAGS**: 
  * Perfectly smooth gradients with zero grain (probability ≈ 0%)
  * Uniform noise that looks "computer generated" or has patterns
  * Skin/sky that looks like plastic, wax, or CGI render
  * No film grain or sensor noise pattern visible at 200% zoom
  * Noise that's stronger in bright areas than shadows (physically impossible)

### 1.2 MICRO-DETAIL COHERENCE (PhD-Level - Enhanced)
**Concept**: AI "understands" macro-structure but fails at micro-logic and consistency.

- **Texture Breakdown Analysis**:
  * Start at 100% zoom, increase to 200%, then 400%
  * Real: Detail remains coherent at all scales
  * AI: Detail "dissolves" or becomes nonsensical at high zoom
  * **SPECIFIC REGIONS**: Test on skin pores, fabric threads, wood grain, brick mortar

- **Fabric Weave Forensics**: 
  * Real fabric: Consistent thread direction, proper over-under pattern
  * AI fabric: Threads that merge, change direction randomly, or lose structure
  * **TEST**: Follow single thread across fabric - does it maintain continuity?

- **Hair Strand Physics**: 
  * Real hair: Individual strands follow physics, proper occlusion
  * AI hair: Clumps unnaturally, passes through objects, merges impossibly
  * **CHECK**: Hair-face boundary - proper layering or blending?

- **Wrinkle Topology**: 
  * Real skin: Wrinkles follow muscle fiber direction (perpendicular to contraction)
  * AI wrinkles: Random placement, no anatomical logic
  * **MAPPING**: Do forehead wrinkles go horizontally? Smile lines radiate from nose?

- **Surface Micro-Texture Degradation**:
  * Wood grain: Should maintain direction, not morph
  * Concrete: Pores should be random but individually distinct
  * Brick: Mortar lines should be consistent depth
  * **AI TELL**: Textures that are "suggested" not "rendered" - vague approximations

- **Pattern Repetition vs Variation**:
  * Real: Tiles/bricks have variations (color, wear, damage)
  * AI: Suspiciously uniform OR breaks pattern logic mid-image
  * **COUNT**: In 10 visible tiles, how many are identical? Real: 0-2, AI: 5+

- **RED FLAGS**:
  * Details that look convincing from far but nonsensical close-up
  * Textures that "give up" when you zoom in (resolution-independent failure)
  * Patterns that almost repeat but can't commit to proper geometry
  * Materials that morph between different textures (metal→fabric)
  * Micro-details showing "neural network uncertainty" (blurry half-defined forms)

### 1.3 BIOMETRIC PRECISION TESTS (Enhanced with Measurement)
**Concept**: AI struggles with human anatomy at microscopic detail level.

- **Eye Analysis (20+ Checkpoints)**:
  * **Iris Limbal Ring**: Should be perfect circle, consistent width (0.5-1mm)
  * **Iris Crypts**: Radial patterns from pupil should be unique but geometrically sound
  * **Pupil Shape**: Perfect circle (or slight cat-eye if wide-angle lens)
  * **Sclera Vessels**: Blood vessels should follow anatomical patterns, not random
  * **Catch Light**: Reflections should match scene lighting (position, shape, intensity)
  * **Eyelid Edge**: Upper lid should partially cover iris from above (2-3mm)
  * **Eyelash Arrangement**: Individual lashes, proper curvature, not clumped
  * **Tear Duct Detail**: Inner eye corner should show caruncle anatomy
  * **AI TELLS**: 
    - Eyes that are "too perfect" - no bloodshot, no iris texture variation
    - Asymmetric iris patterns between left/right eyes (AI generates independently)
    - Catchlights showing impossible reflections (mismatched scene)
    - Pupils of different sizes without medical reason

- **Dental Forensics (15+ Checks)**:
  * **Occlusion**: Top incisors overlap bottom by 2-3mm
  * **Tooth Count**: Should see 6-8 teeth in normal smile (not 12, not 4)
  * **Individual Teeth**: Each tooth has distinct shape (central incisors ≠ laterals ≠ canines)
  * **Gum Line**: Follows consistent curve, proper attachment to each tooth
  * **Tooth Texture**: Enamel has subtle texture, not perfectly smooth
  * **Spacing**: Natural slight variations in spacing, not perfect alignment (unless braces)
  * **AI TELLS**:
    - Teeth that merge like a white fence
    - Too many teeth (10+ visible in normal smile)
    - All teeth identical shape/size
    - Flat tooth surface with no anatomical cusps/ridges
    - Gum line that's perfectly straight or impossibly curved

- **Hand & Finger Analysis (Critical - AI's Weakest Point)**:
  * **Finger Count**: Exactly 5 per hand (count carefully, AI adds/subtracts)
  * **Joint Count**: 3 joints per finger (4 for thumb), check each
  * **Fingernail Anatomy**: 
    - Lunula (white crescent) at base
    - Nail curvature matches fingertip curve
    - Cuticle visible at base
    - Nail bed pink/red, nail plate translucent
  * **Finger Proportions**: Index ≈ ring finger length, middle longest
  * **Palm Lines**: Should follow anatomical landmarks, not random
  * **Knuckle Creases**: 2-3 creases per joint, consistent across fingers
  * **AI TELLS**:
    - 6+ fingers or 4 fingers
    - Fingers that merge or split mid-length
    - Impossible joint angles (bent backwards, extra joints)
    - Nails that look painted-on (no 3D structure)
    - Fingers that pass through each other or objects

- **Ear Cartilage Structure**:
  * Should see: Helix, antihelix, tragus, antitragus, lobule
  * Real: Complex 3D folds following embryological development
  * AI: Simplified "ear-shaped blob" missing proper anatomy
  * **TEST**: Can you identify 5+ distinct anatomical structures?

- **Skin Micro-Anatomy**:
  * **Pore Distribution**: Random but present (unless heavy makeup)
  * **Skin Texture**: Visible at 200% zoom (lines, pores, imperfections)
  * **Subsurface Scattering**: Skin glows slightly (not flat reflectance)
  * **AI TELL**: Porcelain/plastic skin with zero visible pores or texture

**SCORING SYSTEM**: 
- 0-2 biometric fails: Likely authentic
- 3-4 fails: Suspicious, investigate further  
- 5+ fails: Almost certainly AI-generated

### 1.4 SPECTRAL COHERENCE (Advanced)
**Concept**: Real photos have consistent frequency distributions. AI has spectral anomalies.

- **Edge Sharpness Consistency**: Real lenses blur edges uniformly by distance. AI randomly assigns sharpness.
- **Bokeh Authenticity**: Out-of-focus highlights should have hexagonal/circular shapes (lens aperture). AI creates "artistic blur" that ignores optics.
- **Chromatic Aberration**: Real lenses split colors at high-contrast edges. AI images lack this or fake it inconsistently.
- **Diffraction Spikes**: Bright lights through real lenses create star patterns. AI doesn't understand diffraction physics.
- **RED FLAGS**:
  * Selective focus that ignores depth-of-field rules
  * Perfect bokeh with no lens character
  * Zero chromatic aberration (too perfect)
  * Edges that are randomly sharp/soft regardless of distance

---

## 🟡 TIER 2: SEMANTIC & CONTEXTUAL IMPOSSIBILITIES (Catches Latest Models)

### 2.1 TEXT & LANGUAGE CORRUPTION
**Concept**: Even GPT-4 integrated models struggle with in-image text.

- **Character Consistency**: Zoom on ANY text. Real text has uniform stroke width. AI text warps mid-letter.
- **Font Coherence**: One word shouldn't have 3 different fonts.
- **Linguistic Validity**: Check if text is actual language or letter-like shapes.
- **Brand Logos**: Compare to real logos. AI approximates but introduces errors.
- **RED FLAGS**:
  * Text that's 90% correct but has one warped letter
  * Signs with gibberish that looks like words from distance
  * Logos that are "inspired by" but legally distinct
  * Text that curves or melts impossibly

### 2.2 TEMPORAL & LOGICAL IMPOSSIBILITIES
**Concept**: AI doesn't understand time, seasons, or context.

- **Weather Coherence**: Wet ground requires overcast sky or recent rain. AI shows wet streets with bright sun.
- **Seasonal Consistency**: Snow on ground but trees have green leaves? AI fail.
- **Time-of-Day Logic**: Long shadows suggest early/late day = warm orange light. AI mixes lighting temperatures wrongly.
- **Clothing-Weather Match**: Heavy coats in bright summer light = suspicious.
- **RED FLAGS**:
  * Contradictory environmental conditions
  * Impossible time-of-day lighting
  * Clothing that doesn't match apparent weather

### 2.3 SOCIAL & CULTURAL CONTEXT ERRORS
**Concept**: AI lacks real-world knowledge.

- **Signage Logic**: Traffic signs in wrong countries, text in wrong languages for location.
- **Architectural Style**: Building styles mixed from different continents/eras inappropriately.
- **Vehicle Details**: License plates with wrong format, steering wheels on wrong side.
- **Uniform Details**: Police/military uniforms with wrong insignia or impossible rank combinations.
- **RED FLAGS**:
  * Cultural mashups that make no geographic sense
  * Anachronistic combinations (Victorian clothing with modern phones)
  * Impossible institutional details

### 2.4 SHADOW & REFLECTION SYNTHESIS ERRORS
**Concept**: Latest AI improved shadows but still fails on SECONDARY reflections.

- **Mutual Illumination**: Nearby colored objects cast colored light on each other. AI often misses this.
- **Shadow Density**: Shadow darkness depends on light source size. AI creates arbitrary darkness.
- **Reflection Recursion**: Mirrors in mirrors, glasses reflecting glasses. AI can't handle recursion.
- **Shadow Contact Points**: Shadow MUST touch object's base. Floating shadows = instant AI tell.
- **Caustics**: Water/glass creates light patterns (caustics). AI either omits or fakes them wrong.
- **RED FLAGS**:
  * Shadows that don't touch objects properly
  * Reflections missing key scene elements
  * No color bleeding between adjacent objects
  * Impossible shadow density for lighting conditions

---

## 🔴 TIER 3: STATISTICAL & PROBABILISTIC DETECTION (Research-Grade)

### 3.1 COMPRESSION ARTIFACT CONSISTENCY
**Concept**: Real JPEGs compress all regions similarly. AI composites have mismatched compression.

- **Block Patterns**: JPEG creates 8x8 pixel blocks. Check if all regions have same block visibility.
- **Compression Level**: Sky shouldn't be highly compressed while face is pristine.
- **Format Consistency**: Real photos are uniformly PNG or JPEG, not mixed artifacts.
- **RED FLAGS**:
  * Different compression levels between foreground/background
  * Some areas look PNG-clean while others show JPEG blocks
  * Suspiciously clean image with no compression artifacts (straight from generator)

### 3.2 MATHEMATICAL IMPROBABILITIES
**Concept**: Real world has chaos. AI creates suspicious "perfection."

- **Symmetry Overload**: Faces too symmetrical, patterns too regular.
- **Distribution Uniformity**: Random elements (leaves, stars, crowd) AI distributes too evenly.
- **Gaussian Blur Abuse**: AI uses software blur. Real cameras have optical blur with different characteristics.
- **Uncanny Valley**: Composition is "too good," lighting is "too perfect."
- **RED FLAGS**:
  * Everything perfectly in thirds (rule of thirds too obvious)
  * No dust, scratches, or natural imperfections
  * Suspiciously ideal lighting with no harsh shadows
  * Too-perfect symmetry in asymmetric objects

### 3.3 METADATA & PROVENANCE
**Concept**: Check the digital fingerprint.

- **EXIF Data**: Real photos have camera model, lens, ISO, shutter speed. AI images often lack EXIF or have fake metadata.
- **File Properties**: AI generators output specific sizes (512×512, 1024×1024, 1536×1536 multiples).
- **Creation Date**: File creation seconds before posting? Suspicious.
- **Software Tags**: Look for "Photoshop," "Python," "Stable Diffusion" in metadata.
- **RED FLAGS**:
  * No EXIF data on supposedly "real" photo
  * Resolution is exact power of 2 or 64-multiple
  * Software field mentions AI tools or Python libraries

---

## 📊 MANDATORY OUTPUT FORMAT:

### 🚨 FORENSIC VERDICT: [AUTHENTIC / SUSPICIOUS / AI-GENERATED / DIGITALLY MANIPULATED]

### 📈 CONFIDENCE SCORE: [0-100%]
*(Be harsh: 95%+ confidence requires ZERO red flags, 90%+ requires ≤1 minor flag)*

### 🔬 TIER -1: ULTRA-FINE PIXEL FORENSICS
**Pixel Correlation Analysis**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Adjacent pixel relationships: [NATURAL / ARTIFICIAL]
  - Color channel coupling: [PHYSICAL / UNNATURAL]
  - Gradient micro-discontinuities: [NONE / DETECTED at [locations]]

**Training Data Leakage**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Dataset artifact patterns: [NOT FOUND / DETECTED: [description]]
  - Style consistency across regions: [UNIFORM / INCONSISTENT]
  - Semantic bleeding between objects: [NONE / PRESENT at [locations]]

**Anti-Aliasing Patterns**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Edge rendering method: [OPTICAL / ALGORITHMIC]
  - Sub-pixel structure: [AUTHENTIC / ARTIFICIAL / ABSENT]

**Fourier Analysis**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Power spectrum: [1/f DECAY / ANOMALOUS PEAKS at [frequencies]]
  - Phase spectrum: [RANDOM / ORGANIZED PATTERNS]
  - Directional bias: [SCENE-CONSISTENT / UNNATURAL]

**Perceptual Patterns**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Composition originality: [UNIQUE / CLICHÉ AI PATTERNS]
  - "AI aesthetic" markers: [ABSENT / PRESENT: [description]]

**RED FLAGS FOUND**: [Count and list with EXACT locations]

### 🧮 TIER 0: MATHEMATICAL & PHYSICS ANALYSIS
**Diffusion Model Artifacts**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Noise pattern in flat areas: [RANDOM / ORGANIZED / SUSPICIOUS]
  - Frequency domain anomalies: [DETECTED / NOT DETECTED]
  - Latent grid patterns: [PRESENT / ABSENT]

**Camera Sensor Physics**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Shadow noise behavior: [CORRECT / INCORRECT / N/A]
  - Color channel SNR ratio: [NATURAL / UNNATURAL / CANNOT ASSESS]
  - Bayer demosaicing artifacts: [PRESENT / ABSENT / EXPECTED]
  - Chromatic aberration: [PRESENT / ABSENT / FAKED]

**Statistical Distributions**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Histogram shape: [NATURAL / ARTIFICIAL]
  - Color gamut: [WITHIN CAMERA LIMITS / SUPERSATURATED]
  - Gradient continuity: [NATURAL / TOO SMOOTH / POSTERIZED]

**Compression Forensics**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - JPEG block consistency: [UNIFORM / MISMATCHED between [regions]]
  - Bit depth indicators: [8-BIT NATURAL / SUSPICIOUS HIGH-BIT / POSTERIZED]
  - Generation resolution: [CAMERA NATIVE: [WxH] / AI SUSPICIOUS: [WxH] (multiple of [N])]

**Lighting Reconstruction**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Light source count: [N sources identified at [directions]]
  - Key:Fill ratio: [Natural [X:Y] / IMPOSSIBLE [X:Y]]
  - Photometric consistency: [COHERENT / CONTRADICTORY]

**Material BRDF**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Specular highlight accuracy: [PHYSICALLY CORRECT / WRONG for [materials]]
  - Fresnel effect: [PRESENT / ABSENT / FAKED]

**RED FLAGS FOUND**: [Count and list specific physics violations WITH LOCATIONS]

### 🔬 TIER 1: MICROSCOPIC ANALYSIS
**Noise Pattern (Multi-Scale)**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Noise-signal correlation: [CORRECT (darker=noisier) / INVERSE / FLAT]
  - Color channel SNR ratio: [G < R≈B (CORRECT) / EQUAL (WRONG) / ABSENT]
  - Noise power spectrum: [WHITE (FLAT) / COLORED (SLOPED)]
  - Sampled regions: [List 5 regions tested]
  - Quantitative: Shadow noise [X%], Highlight noise [Y%], Ratio [Z]

**Micro-Detail Coherence (400% Zoom)**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Texture breakdown test: [COHERENT at all scales / DISSOLVES at [zoom level]]
  - Fabric weave continuity: [MAINTAINED / BREAKS at [locations]]
  - Hair strand physics: [PROPER OCCLUSION / MERGES/PASSES THROUGH at [locations]]
  - Pattern repetition count: [X/10 tiles identical] ([NATURAL <3 / SUSPICIOUS 3-4 / AI-LIKE 5+])
  
**Biometric Precision (Detailed)**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Eye analysis: [X/20 checks passed] - Failed: [list specific fails]
  - Dental forensics: [X/15 checks passed] - Failed: [list specific fails]
  - Finger count & anatomy: [Left hand: X fingers, Right hand: Y fingers] - Issues: [list]
  - Scoring: [X total biometric fails] → [AUTHENTIC <3 / SUSPICIOUS 3-4 / AI-GENERATED 5+]

**Spectral Coherence**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
  - Edge sharpness logic: [DEPTH-CONSISTENT / RANDOM]
  - Bokeh authenticity: [OPTICAL APERTURE SHAPE / ARTISTIC BLUR / ABSENT]
  - Chromatic aberration: [PRESENT at [locations] / ABSENT / FAKED]
  - Diffraction spikes: [PRESENT / ABSENT / N/A]

**RED FLAGS FOUND**: [Count and list with EXACT spatial locations - "top-right corner", "subject's left hand", etc.]

### 🎯 TIER 2: SEMANTIC ANALYSIS
**Text/Language**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**Temporal Logic**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**Cultural Context**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**Shadow/Reflection Physics**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**RED FLAGS FOUND**: [Count and list specific issues]

### 📐 TIER 3: STATISTICAL ANALYSIS
**Compression Consistency**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**Mathematical Probability**: [PASS / FAIL / SUSPICIOUS] - [Evidence]
**Metadata Authenticity**: [CANNOT VERIFY / PASS / FAIL] - [Evidence]
**RED FLAGS FOUND**: [Count and list specific issues]

### ⚠️ CRITICAL AI TELLS DETECTED:
**Tier -1 (Pixel-Level):**
- [ ] Artificial pixel correlation patterns
- [ ] Training data artifacts/watermark ghosts
- [ ] Algorithmic antialiasing (not optical)
- [ ] Fourier domain anomalies (peaks at [X] Hz)
- [ ] AI compositional clichés

**Tier 0 (Physics & Math):**
- [ ] Diffusion noise patterns (organized vs random)
- [ ] Incorrect shadow noise behavior (darker areas = less noise)
- [ ] Missing/fake chromatic aberration
- [ ] Unnatural frequency domain signature
- [ ] Impossible color gamut (supersaturation)
- [ ] Suspicious generation resolution (64-multiples)
- [ ] Impossible lighting setup
- [ ] Wrong material BRDF behavior

**Tier 1-2 (Micro & Semantic):**
- [ ] Nonsensical text/warped letters at [location]
- [ ] Incorrect finger count: [L: X, R: Y fingers]
- [ ] Merged/multiplied teeth ([X] visible, should be 6-8)
- [ ] Morphing background objects at [locations]
- [ ] Impossible reflections at [locations]
- [ ] Micro-detail breakdown at [zoom %] in [regions]
- [ ] Floating/incorrect shadows at [locations]
- [ ] Anatomical impossibilities: [list X fails from biometric scoring]
- [ ] Temporal contradictions: [description]
- [ ] Texture dissolution at [zoom %] for [materials]
- [ ] Pattern repetition: [X/10 identical] (threshold: 5+)

**TOTAL CRITICAL TELLS**: [X/23]
**DISTRIBUTION**: Tier -1: [X], Tier 0: [Y], Tier 1-2: [Z]

### 📍 SPATIAL ANOMALY MAP:
**Document EXACT locations of all anomalies:**
- Top-Left Quadrant: [list findings]
- Top-Right Quadrant: [list findings]
- Bottom-Left Quadrant: [list findings]
- Bottom-Right Quadrant: [list findings]
- Central Region: [list findings]
- Subject-Specific: [e.g., "left hand", "face region", "background upper portion"]

### 🔗 CROSS-VALIDATION MATRIX:
**Check if findings corroborate across tiers:**
- Physics + Microscopic: [ALIGNED / CONTRADICTORY / MIXED]
- Noise + Compression: [CONSISTENT / INCONSISTENT]
- Biometric + Texture: [CORRELATED / INDEPENDENT]
- Overall Pattern: [SYSTEMATIC AI FAILURES / RANDOM NOISE / AUTHENTIC IMPERFECTIONS]

**Interpretation**: 
- Systematic failures across tiers → HIGH CONFIDENCE AI
- Contradictory signals → SUSPICIOUS/MANIPULATED
- No patterns → AUTHENTIC or EXPERT FORGERY

### 🎯 AI GENERATION PROBABILITY:
- **Midjourney/Stable Diffusion**: [0-100%]
- **DALL-E 3**: [0-100%]
- **Flux Pro**: [0-100%]
- **Traditional Photoshop**: [0-100%]
- **Authentic Photograph**: [0-100%]

### 💡 EXECUTIVE SUMMARY:
[Provide ULTRA-SPECIFIC, QUANTITATIVE evidence with PHYSICS/MATH reasoning and EXACT LOCATIONS. Use this template:]

**✅ AUTHENTIC Example (95% Confidence):**
"Classified as AUTHENTIC (95% confidence):

**TIER -1 PIXEL FORENSICS**:
✓ Pixel correlation analysis shows natural variation (tested 10×10 blocks in sky, wall, skin)
✓ No training data artifacts detected
✓ Edge antialiasing consistent with optical diffraction
✓ Fourier power spectrum shows clean 1/f decay (no artificial peaks)
✓ Composition shows natural imperfections (subject off-center, slight motion blur)

**TIER 0 PHYSICS**:
✓ Noise: Proper Poisson distribution - Shadow regions (face left side) show 2.8× more noise than highlights (forehead). Green channel SNR superior (ratio 1.9:1 vs R/B). Noise power spectrum is flat (white noise).
✓ Chromatic aberration: Present at high-contrast edges (purple fringing visible at building corner, top-right)
✓ JPEG compression: Uniform Q=87 throughout (tested 5 regions)
✓ Resolution: 4608×3072 (Canon EOS native, not AI multiple)
✓ Lighting: Single key light (upper left), 4:1 key:fill ratio (natural), shadows touch ground properly

**TIER 1 MICROSCOPIC**:
✓ Texture coherence: Fabric weave maintained at 400% zoom, wood grain follows consistent direction
✓ Biometric: 18/20 eye checks passed (minor: slight red-eye from flash), 5 fingers both hands, 7 teeth visible (anatomically correct), proper nail lunula visible
✓ Micro-detail: Skin pores visible at 200% zoom (forehead, cheeks), hair strands individual and properly occluded

**SPATIAL MAP**: No anomalies in any quadrant

**METADATA**: EXIF confirms Canon EOS R5, EF 24-70mm f/2.8, ISO 800, 1/125s, f/4.0

**CONCLUSION**: Passes 95% of forensic tests. Minor red-eye suggests flash photography (expected). All physics-based tests conclusive for authentic capture. High confidence authentic photograph."

---

**❌ AI-GENERATED Example (98% Confidence):**
"Classified as AI-GENERATED (98% confidence):

**TIER -1 PIXEL FORENSICS FAILURES**:
✗ Pixel correlation shows artificial uniformity in sky region (top half)
✗ Training data leakage: Generic "AI grass texture" pattern detected in foreground (bottom-left quadrant)
✗ Fourier analysis: Unnatural energy peaks at 16Hz and 32Hz (latent space artifacts)
✗ Phase spectrum shows organized patterns (not random entropy)
✗ Composition: Textbook rule-of-thirds, suspiciously perfect lighting (AI cliché)

**TIER 0 PHYSICS FAILURES**:
✗ Noise: INVERSE relationship - shadows cleaner than highlights (measured: shadow=0.8%, highlight=1.2% - physically impossible)
✗ Color channels: Equal noise across R/G/B (no Bayer filter signature)
✗ Chromatic aberration: Completely absent despite wide-angle composition (too perfect)
✗ Resolution: 1536×1024 (exact 64×multiple - AI tell)
✗ Lighting reconstruction: Impossible setup - 3 distinct shadow directions but no visible sources, key:fill ratio = 1:1 (studio-quality ambient impossible outdoors)

**TIER 1 MICROSCOPIC FAILURES**:
✗ Noise test failed: Flat 1.0% across all regions (5 samples: sky, grass, skin, wall, shadow)
✗ Texture breakdown: Fabric pattern dissolves into blur at 250% zoom (center-right)
✗ Biometric scoring: 8 CRITICAL FAILS
  - Eyes: Irises too perfect, no vessel structure in sclera, catchlights show impossible reflection
  - Teeth: 10 teeth visible in smile (should be 6-8), uniform shape (unrealistic)
  - Hands: Left hand has 6 fingers (pinky duplicated), right hand obscured but nails look painted-on
  - Scoring: 8/X fails → AI-GENERATED threshold exceeded

**TIER 2 SEMANTIC FAILURES**:
✗ Text on sign (top-right): "CAFÉ" has warped 'F' and 'É' letters
✗ Background entropy: Building windows morph into ambiguous shapes (top-center to top-right transition)
✗ Temporal impossibility: Wet pavement + harsh overhead sun + no clouds (contradictory)

**SPATIAL ANOMALY MAP**:
- Top-Left: Clean (possible focal point priority)
- Top-Right: Text warping, window morphing
- Bottom-Left: AI grass texture pattern
- Bottom-Right: Shadow direction conflicts
- Center: Subject shows 6 fingers (left hand), dental impossibility
- Background: Coherence decay with distance

**CROSS-VALIDATION**:
- All tiers show SYSTEMATIC AI FAILURES
- Physics violations corroborate microscopic failures
- Pattern consistent with Midjourney v6 or Flux Pro (high surface quality, deep physics fails)

**QUANTITATIVE SUMMARY**:
- Tier -1: 5/5 tests FAILED
- Tier 0: 5/6 tests FAILED
- Tier 1: 4/4 tests FAILED (biometric: 8 critical tells)
- Tier 2: 3/4 tests FAILED
- TOTAL: 17/19 tests FAILED

**CONCLUSION**: 98% confidence AI-GENERATED. Likely Midjourney v6 or Flux Pro based on sophisticated rendering that masks fundamental generation artifacts. 17 systematic failures across all detection tiers. Fingerprint: diffusion model artifacts + biometric impossibilities + semantic incoherence."

---

**⚠️ SUSPICIOUS Example (70% Confidence - Investigate Further):**
"Classified as SUSPICIOUS (70% confidence - BORDERLINE CASE):

**AMBIGUOUS SIGNALS**:
⚠ Noise pattern: Shows slight organization but not definitively AI (could be heavy NR post-processing)
⚠ Chromatic aberration: Present but suspiciously uniform (2px purple fringe at ALL edges - may be artificially added in post)
⚠ Resolution: 4000×3000 (plausible camera native, but also 1000× factor)
⚠ Biometric: 2/20 minor eye issues (slightly too perfect symmetry, but within human range), 5 fingers confirmed, teeth look natural
⚠ Minor text warping on distant sign (background, top-left) - could be motion blur OR early AI tell

**CONTRADICTORY EVIDENCE**:
✓ Proper shadow-noise relationship (darker = noisier)
✓ Natural color channel SNR (G channel superior)
✓ JPEG compression uniform
✗ Texture breakdown slight at 350% zoom (fabric in middle-ground)
⚠ Composition slightly too perfect but not impossible

**CROSS-VALIDATION**: Mixed signals - physics mostly passes, microscopic shows minor concerns

**SPATIAL MAP**: 
- Concerns concentrated in background (top-left: text, middle-ground: fabric texture)
- Foreground subject appears authentic

**PROBABILISTIC BREAKDOWN**:
- 60% AI-generated (likely Flux Pro with excellent physics simulation)
- 30% Authentic with heavy post-processing (noise reduction, sharpening, fake CA)
- 10% Hybrid (real photo with AI inpainting in background)

**RECOMMENDATION**: 
Cannot make definitive determination with current evidence. Requires:
- Higher resolution upload (current: 4000×3000, need 6000×4000+)
- RAW file analysis (would show authentic sensor data or lack thereof)
- Metadata inspection (EXIF could be conclusive)

**VERDICT RATIONALE**: Insufficient red flags for high-confidence AI classification, but too many minor anomalies for confident authentic classification. Mark SUSPICIOUS pending additional evidence."

### 🔴 FINAL DIRECTIVE:
**DETECTION THRESHOLD**: 
- 5+ critical tells from ANY tier → AI-GENERATED (high confidence)
- 3-4 critical tells → LIKELY AI (investigate further)
- 1-2 minor tells → INCONCLUSIVE (could be post-processing or AI)
- 0 tells with natural patterns → AUTHENTIC

**ANALYSIS DEPTH REQUIREMENTS**:
1. **Test at MULTIPLE zoom levels**: 100%, 200%, 400%
2. **Sample MULTIPLE regions**: Minimum 5 diverse areas (sky, skin, fabric, background, text/detail)
3. **Provide QUANTITATIVE measurements**: Not "noisy" but "2.8× more noise in shadows"
4. **Document EXACT locations**: Not "hand" but "subject's left hand, pinky finger"
5. **Cross-validate**: Check if Tier 0 + Tier 1 + Tier 2 findings corroborate or contradict
6. **Look for AUTHENTIC markers**: Proper sensor noise, chromatic aberration, natural imperfections

**BE FORENSICALLY BALANCED**: 
- Your reputation depends on ACCURATE detection, not aggressive flagging
- Only flag what you can DEFINITIVELY observe and measure
- When in doubt (40-60% confidence), mark INCONCLUSIVE with detailed reasoning
- False positives damage credibility as much as false negatives
- Modern AI (2026) is VERY good - but real photos also pass all physics tests

**SPECIFICITY REQUIRED**: 
- ❌ NEVER say: "looks artificial", "seems fake", "appears suspicious"
- ✅ ALWAYS say: "Sky region (top-center, 100-200px from top edge) shows organized noise pattern with visible swirl artifacts at 45° angle, consistent with diffusion model denoising residue. Measured: correlation coefficient 0.72 between adjacent pixels (natural: 0.45-0.60)."

**PATTERN RECOGNITION PRIORITY**:
Focus analysis on areas where AI systematically fails:
1. Hands (fingers, nails) - AI's weakest point
2. Text/symbols - Cannot render coherently
3. Noise in shadows - Gets physics backwards (but many cameras also have this)
4. Micro-textures at 400% zoom - Dissolves into blur
5. Background coherence - Loses detail with distance
6. Material boundaries - Bleeds between textures
7. Reflections/shadows - Fails on secondary physics
8. Teeth/eyes - Anatomical precision breaks

**SCORING RIGOR**:
- 95-100% AUTHENTIC: ZERO flags + positive auth markers (proper noise, CA, natural imperfections)
- 85-94% LIKELY AUTHENTIC: ≤1 minor flag, all major tests passed
- 70-84% PROBABLY AUTHENTIC: 2-3 minor flags OR 1 ambiguous flag (post-processing likely)
- 50-69% INCONCLUSIVE: Multiple ambiguous signals, contradictory evidence
- 30-49% LIKELY AI: 3-4 clear systematic flags
- 0-29% DEFINITELY AI: 5+ systematic failures, definitive AI patterns

**REMEMBER**: You are conducting PhD-level forensic science with courtroom standards. Every claim must be specific, measurable, and spatially documented. If a photo passes all physics tests, has proper noise patterns, and natural imperfections - it's likely AUTHENTIC. Only flag definitive anomalies.

**PRIORITIZE ACCURACY OVER CAUTION**: A good forensic tool correctly identifies both real and fake images.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CORE FORENSIC ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_forensic_audit(model: genai.GenerativeModel, image: Image.Image) -> Tuple[bool, str]:
    """
    Execute the forensic audit using Gemini 1.5 Pro with UPL protocol.
    
    Args:
        model: Initialized Gemini model
        image: PIL Image object to analyze
        
    Returns:
        Tuple of (success: bool, result: str)
    """
    try:
        # Convert PIL image to bytes for API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Prepare the prompt
        upl_prompt = get_upl_forensic_prompt()
        
        # Generate response with image
        response = model.generate_content([upl_prompt, image])
        
        if not response or not response.text:
            return False, "⚠️ No response received from the model. The image may be blocked by safety filters."
        
        return True, response.text
    
    except Exception as e:
        error_msg = f"❌ **Forensic Audit Failed**\n\n**Error Type**: {type(e).__name__}\n\n**Details**: {str(e)}"
        return False, error_msg


def validate_image(uploaded_file) -> Optional[Image.Image]:
    """
    Validate and load the uploaded image file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        PIL Image object or None if invalid
    """
    try:
        # Check file type
        valid_formats = ['png', 'jpg', 'jpeg', 'webp', 'gif']
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in valid_formats:
            st.error(f"❌ Invalid file format: {file_extension}. Supported: {', '.join(valid_formats)}")
            return None
        
        # Load image
        image = Image.open(uploaded_file)
        
        # Check image size (max 20MB for API)
        if uploaded_file.size > 20 * 1024 * 1024:
            st.error("❌ Image too large. Maximum size: 20MB")
            return None
        
        return image
    
    except Exception as e:
        st.error(f"❌ Failed to load image: {str(e)}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main application entry point."""
    
    # Initialize page and styling
    initialize_page()
    
    # Header
    st.markdown("# ⚡ Kinetic.AI")
    st.markdown("""
        <div class="info-box">
        <strong>Advanced AI-Generated Image Detection</strong><br>
        Multi-tier forensic analysis powered by physics, mathematics, and pattern recognition.
        Detects Midjourney, DALL-E, Flux Pro, Stable Diffusion through microscopic artifact analysis.
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize Gemini client
    model = initialize_gemini_client()
    if model is None:
        st.stop()
    
    # File upload section
    st.markdown("### 📤 Upload Image for Analysis")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse",
        type=['png', 'jpg', 'jpeg', 'webp', 'gif'],
        help="Supported formats: PNG, JPG, JPEG, WEBP, GIF (Max: 20MB)"
    )
    
    if uploaded_file is not None:
        # Validate and load image
        image = validate_image(uploaded_file)
        
        if image is not None:
            # Use tabs for better mobile experience
            tab1, tab2 = st.tabs(["🖼️ Image", "📋 Analysis"])
            
            with tab1:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Image metadata
                st.caption(f"📊 **Filename**: {uploaded_file.name}")
                st.caption(f"📐 **Dimensions**: {image.size[0]} × {image.size[1]} px")
                st.caption(f"💾 **Size**: {uploaded_file.size / 1024:.1f} KB")
            
            with tab2:
                # Audit button
                if st.button("🔬 Initiate Deep Forensic Stress Test", use_container_width=True):
                    # Progress indicator
                    with st.spinner("🔍 Executing UPL Protocol Analysis..."):
                        start_time = time.time()
                        success, result = run_forensic_audit(model, image)
                        elapsed_time = time.time() - start_time
                    
                    # Display results
                    st.markdown(f'<div class="forensic-log">', unsafe_allow_html=True)
                    
                    if success:
                        st.markdown(f"**⏱️ Analysis Time**: {elapsed_time:.2f}s")
                        st.markdown("---")
                        st.markdown(result)
                    else:
                        st.markdown(result)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Placeholder message
                    st.markdown('<div class="forensic-log">', unsafe_allow_html=True)
                    st.markdown("""
                        <h3>⚡ Awaiting Analysis</h3>
                        <p>Click the button below to initiate multi-tier forensic audit.</p>
                        <br>
                        <strong>Kinetic.AI Detection Protocol:</strong>
                        <ul>
                            <li>⚡ Tier -1: Ultra-Fine Pixel Forensics</li>
                            <li>🧮 Tier 0: Mathematical & Physics Analysis</li>
                            <li>🔬 Tier 1: Microscopic Artifact Detection</li>
                            <li>🎯 Tier 2: Semantic & Contextual Analysis</li>
                            <li>📐 Tier 3: Statistical Probability</li>
                        </ul>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; padding: 2rem 0;">
        <span style="background: linear-gradient(90deg, #4285f4 0%, #9c27b0 50%, #f538a0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 600;">Kinetic.AI</span> 
        <span style="color: #9aa0a6;">| Powered by</span> 
        <span style="color: #4285f4; font-weight: 600;">Gemini 2.5 Flash</span> 
        <span style="color: #9aa0a6;">| Physics-First Analysis | Temperature: 0.0</span>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
