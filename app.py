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
    Advanced AI detection for state-of-the-art generators (Midjourney v6, DALL-E 3, Flux Pro).
    """
    return """
# FORENSIC IMAGE AUDIT: UNIVERSAL PHYSICAL LAW (UPL) PROTOCOL v3.0
## ADVANCED AI GENERATION DETECTION SYSTEM
### Designed to detect: Midjourney v6, DALL-E 3, Flux Pro, Stable Diffusion XL, Firefly

You are an ELITE forensic image analyst with PhD-level expertise in computer vision, digital forensics, neural network artifacts, and statistical pattern recognition.

🎯 **MISSION**: Conduct EXHAUSTIVE multi-layered analysis to detect even the most sophisticated AI-generated images through microscopic examination and pattern correlation.

⚠️ **PHILOSOPHY**: Assume AI-generation until proven authentic through MULTIPLE independent verification channels. Use cross-validation between detection tiers.

🔬 **ANALYSIS APPROACH**:
1. **Multi-Scale Inspection**: Examine at 100%, 200%, 400% zoom levels
2. **Cross-Correlation**: Findings from one tier must corroborate others
3. **Pattern Matching**: Look for systematic vs random anomalies
4. **Spatial Mapping**: Document EXACT locations (coordinates/regions)
5. **Probabilistic Scoring**: Weight evidence by reliability and clarity

---

## 🔍 TIER -1: ULTRA-FINE PIXEL-LEVEL FORENSICS (Expert Analyst Layer)
### Deep Pattern Recognition & Minor Artifact Detection

**CRITICAL**: This tier catches the 5% of sophisticated AI that passes initial screening.

### -1.1 PIXEL CORRELATION ANALYSIS
**Concept**: Real photos have natural pixel-to-pixel relationships. AI creates artificial correlations.

- **Local Pixel Statistics**:
  * Real photos: Adjacent pixels correlate based on actual material properties
  * AI: Artificial smoothness or random discontinuities at pixel level
  * **Test**: Sample 10×10 pixel blocks across image - check for consistent correlation coefficients
  
- **Color Channel Coupling**:
  * Real: R, G, B channels show physical coupling (same light source)
  * AI: Channels sometimes generated semi-independently → unnatural coupling patterns
  * **Look for**: One channel showing detail absent in others (impossible physically)

- **Gradient Continuity**:
  * Real: Gradients change smoothly except at material boundaries
  * AI: Micro-discontinuities where neural network patches meet
  * **Check**: Smooth gradients (sky, skin) for tiny "seams" or abrupt changes

### -1.2 TRAINING DATA LEAKAGE PATTERNS
**Concept**: AI models memorize fragments from training data, leaving fingerprints.

- **Dataset Artifacts**:
  * Common training sets (LAION-5B, ImageNet) have specific artifact patterns
  * Watermark ghosts from scraped internet images
  * Repeated texture motifs across different image regions
  * **Red Flag**: Seeing "familiar but generic" patterns (AI's "favorite" textures)

- **Style Transfer Remnants**:
  * AI sometimes shows vestiges of multiple art styles in one image
  * Inconsistent rendering styles between foreground/background/details
  * **Check**: Does the artistic "hand" change between regions?

- **Semantic Bleeding**:
  * Objects adopt characteristics of nearby objects (neural network confusion)
  * Example: Metal object with fabric texture, glass with stone properties
  * **Test**: Do material properties remain consistent or blend?

### -1.3 ANTI-ALIASING & SUB-PIXEL RENDERING
**Concept**: Real cameras/lenses create natural antialiasing. AI synthesizes it algorithmically.

- **Edge Antialiasing Patterns**:
  * Real: Natural light diffraction creates specific edge profiles
  * AI: Software antialiasing (too perfect, wrong pixel arrangement)
  * **Test**: High-contrast edges should show color fringing + gradual transition, not just grayscale blend

- **Sub-Pixel Structure**:
  * Real LCD/camera: RGB sub-pixel arrangement visible at extreme zoom
  * AI: No sub-pixel structure OR artificially added structure
  * **Check**: Does extreme zoom reveal authentic sensor/display structure?

### -1.4 FOURIER TRANSFORM DEEP DIVE
**Concept**: Frequency domain reveals generation artifacts invisible in spatial domain.

- **Power Spectrum Analysis**:
  * Real photos: Smooth 1/f power law decay
  * AI: Bumps, peaks, or plateaus at specific frequencies
  * **Pattern**: Look for artificial "energy shelves" at 8, 16, 32, 64 cycles

- **Phase Spectrum Anomalies**:
  * Real: Random phase relationships (natural entropy)
  * AI: Organized phase patterns (neural network periodicity)
  * **Test**: Phase spectrum should look like TV static, not organized patterns

- **Directional Frequency Analysis**:
  * Real: Frequency content matches scene geometry
  * AI: Unnatural directional bias in frequency domain
  * **Red Flag**: Horizontal/vertical frequency dominance not matching scene structure

### -1.5 PERCEPTUAL HASH COLLISION DETECTION
**Concept**: AI generators have "preferred solutions" - similar images share hash patterns.

- **Pattern Repetition**:
  * Check if image regions resemble common AI generator outputs
  * AI has "default" ways of rendering eyes, hands, clouds, trees
  * **Mental Test**: Does this look like a "typical" AI image of this category?

- **Compositional Clichés**:
  * AI follows training data composition patterns obsessively
  * Over-reliance on rule-of-thirds, centered subjects, ideal lighting
  * Real photos have more chaos, imperfection, poor framing
  * **Red Flag**: Everything is "too well composed" - no happy accidents

---

## 🧮 TIER 0: MATHEMATICAL & PHYSICS-BASED GENERATION ANALYSIS (Foundation Layer)
### Enhanced with Cross-Pattern Correlation

**ADDITION TO PREVIOUS TIER 0**: Apply these CROSS-VALIDATION checks:

### 0.7 MULTI-POINT CROSS-VALIDATION
**Concept**: Independent tests should corroborate each other.

- **Consistency Checks**:
  1. If noise pattern suggests AI → Check if chromatic aberration also suspicious
  2. If resolution suggests AI (64-multiple) → Verify compression consistency
  3. If shadows fail → Check if reflections also fail
  4. If texture breaks down → Check if adjacent textures also fail

- **Contradiction Detection**:
  * Real photos: All physics tests align consistently
  * AI/Manipulated: Tests give contradictory signals
  * **Example**: Perfect lens characteristics BUT wrong noise → composite image

### 0.8 LIGHTING RECONSTRUCTION
**Concept**: Reverse-engineer the lighting setup. Real scenes have physical light sources.

- **Light Source Counting**:
  * Count distinct shadow directions → should match visible/implied light sources
  * Check specular highlights → should point to same light origins
  * Verify fill light ratios → natural ratios (key:fill = 2:1 to 8:1)
  * **AI Tell**: Impossible lighting setups (3 suns, ambient light with hard shadows)

- **Photometric Stereo Check**:
  * Object shape should be consistent with its shading
  * Curved surfaces: Shading gradient should match curvature
  * **Red Flag**: Flat shading on curved objects, or 3D shading on flat surfaces

### 0.9 MATERIAL BIDIRECTIONAL REFLECTANCE (BRDF)
**Concept**: Materials reflect light according to physical laws. AI approximates.

- **Specular Highlight Shape**:
  * Metal: Sharp, colored highlights
  * Plastic: Soft, white highlights
  * Skin: Subsurface scattering (soft, warm glow)
  * **AI Fail**: Materials with wrong highlight characteristics

- **Fresnel Effect**:
  * Surfaces are more reflective at grazing angles
  * Check edges of reflective objects for increased reflection
  * **Test**: Do windows/water/glass show proper Fresnel behavior?

### 0.10 TEMPORAL CONSISTENCY (If Multiple Frames/Elements)
**Concept**: Elements that should relate temporally must be consistent.

- **Motion Consistency**:
  * Motion blur direction must match action
  * Motion blur amount must match speed
  * **AI Tell**: Static objects with motion blur, or moving objects without

- **Causal Relationships**:
  * Smoke rises from fire source
  * Water splashes originate from impact point
  * **Check**: Do dynamic elements have proper causal origins?

---

## 🧮 TIER 0: MATHEMATICAL & PHYSICS-BASED GENERATION ANALYSIS (Foundation Layer)
### Understanding: AI Generation vs Camera Physics

**CRITICAL CONTEXT**: This tier examines HOW the image was created at a fundamental level.

### 0.1 DIFFUSION MODEL ARTIFACTS (Stable Diffusion, Midjourney, DALL-E 3, Flux)
**Physics**: AI starts with random noise and iteratively denoises it over ~50 steps using learned patterns.

- **Latent Space Fingerprints**: Diffusion models work in compressed latent space, then decode to pixels. This creates:
  * **Frequency Band Anomalies**: AI has unnatural energy distribution in mid-frequencies (8-32 cycles/image)
  * **Denoising Residue**: Subtle "swirl patterns" or "flow fields" visible in flat areas (sky, walls)
  * **Latent Grid**: Sometimes visible 8×8 or 16×16 grid patterns in uniform areas
  
- **Forward Diffusion Traces**: Check flat uniform areas (blue sky, white walls):
  * Real photos: Random sensor noise (Poisson distribution)
  * AI images: Residual noise patterns that look "too organized" or have directional flow
  
- **Noise Schedule Artifacts**: 
  * Early denoising steps affect large structures, late steps add fine detail
  * AI sometimes shows "hierarchical detail mismatch" - large forms are perfect but small details are incoherent
  
**TEST**: Examine the sky, walls, or any flat color area. Apply mental "high-pass filter":
- **REAL**: Pure random sparkle, no patterns
- **AI**: Subtle swirls, organized noise, or suspicious smoothness

### 0.2 GAN FREQUENCY DOMAIN ARTIFACTS (Legacy but still present)
**Physics**: Generative Adversarial Networks create images through adversarial training, leaving spectral signatures.

- **Checkerboard Artifacts**: GANs using transposed convolution create checkerboard patterns in frequency domain
  * Visible as: Subtle grid-like patterns in flat areas
  * Peak at specific frequencies (typically 2× the upsampling factor)
  
- **Frequency Clamping**: AI has unnaturally sharp cutoffs in frequency spectrum:
  * Real photos: Gradual frequency falloff based on lens MTF (modulation transfer function)
  * AI: Artificial frequency ceiling where high frequencies abruptly disappear
  
- **Phase Coherence**: 
  * Real photos: Random phase relationships between frequencies
  * AI: Suspiciously coherent phases (artifacts of convolutional structure)

**TEST**: Look for repeated patterns or "screen door effect" in uniform areas.

### 0.3 CAMERA SENSOR PHYSICS vs AI SYNTHESIS

#### Real Camera Physics:
1. **Bayer Filter Pattern**: Cameras use RGBG pattern (2× green sensors). This creates:
   - Green channel has higher SNR (signal-to-noise ratio)
   - Slight green bias in demosaicing
   - Zipper artifacts along edges (color aliasing)

2. **Photon Shot Noise**: Light arrives as discrete photons following Poisson statistics:
   - Noise magnitude = √(signal intensity)
   - Darker areas have MORE noise (proportionally)
   - Each color channel has independent noise

3. **Read Noise**: Electronics add Gaussian noise independent of signal
   - Fixed-pattern noise (hot/dead pixels)
   - Consistent across frames from same camera

4. **Optical Aberrations**:
   - Chromatic aberration (color fringing at edges)
   - Vignetting (darker corners)
   - Lens distortion (barrel/pincushion)
   - MTF falloff (sharpness decreases from center)

#### AI Synthesis Characteristics:
1. **No Bayer Pattern**: AI synthesizes RGB directly, no demosaicing artifacts
2. **Statistically Perfect Noise**: AI adds noise that's "too uniform"
   - Equal noise across all channels (wrong!)
   - Noise doesn't follow Poisson statistics
   - No signal-dependent noise behavior
3. **Impossible Optics**: No chromatic aberration, no vignetting, or fakes them inconsistently
4. **Frequency Response**: AI doesn't follow lens MTF curves

**CRITICAL TESTS**:
- **Shadow Noise Test**: Real photos have MORE noise in shadows. AI often has equal or less noise in shadows.
- **Color Channel SNR**: Real photos have better green channel. AI has equal R/G/B noise.
- **Chromatic Aberration**: Zoom on high-contrast edges. Real lenses split colors. AI doesn't (or fakes it wrong).

### 0.4 STATISTICAL DISTRIBUTION ANALYSIS

#### Histogram Analysis:
**Real Photos**:
- Smooth, gradual histograms
- Clipping at 0 or 255 if overexposed (natural)
- Channel histograms have different shapes

**AI Images**:
- Suspiciously "perfect" histogram with no clipping
- All channels have similar histogram shapes (unnatural)
- May show "histogram gaps" (posterization from limited training data)

#### Color Space Anomalies:
**Real Photos**:
- Colors follow natural illuminant constraints (D65 daylight, tungsten, etc.)
- Impossible colors (outside camera gamut) never appear
- Metamerism effects (colors that match under one light change under another)

**AI Images**:
- Colors sometimes exceed natural gamut (supersaturated)
- Ignores metamerism (all lighting conditions look the same)
- May create "impossible colors" that no camera can capture

#### Gradient Smoothness:
**Real Photos**: 
- Continuous, smooth gradients (limited by bit depth but consistent)
- Banding only in extreme cases (8-bit limitations)

**AI Images**:
- Unnaturally smooth gradients (no quantization noise)
- OR sudden posterization (neural network discretization)
- Gradients that "give up" and become flat

### 0.5 COMPRESSION & ENCODING FORENSICS

**Real Photo Pipeline**:
1. Sensor → RAW data (12-14 bit per channel)
2. Demosaicing → RGB (still high bit depth)
3. JPEG compression → 8-bit, 8×8 DCT blocks
4. Result: Uniform compression artifacts throughout

**AI Generation Pipeline**:
1. Latent space → Decoder → RGB (synthesized at target resolution)
2. Often saved as PNG initially (no compression)
3. Later converted to JPEG → inconsistent compression

**TESTS**:
- **Block Artifact Consistency**: All regions should have similar JPEG block visibility
  * AI composites: Foreground pristine, background heavily compressed (different sources)
- **Bit Depth Clues**: Real photos show subtle banding in gradients (8-bit limitation)
  * AI: Too-smooth gradients (synthesized in high bit depth)
- **Generation Resolution**: 
  * Real photos: Native sensor resolution (e.g., 6000×4000, 4608×3456)
  * AI: Suspiciously round numbers (1024×1024, 1536×1536, 512×768) or multiples of 64

### 0.6 EDGE & STRUCTURE COHERENCE

**Real Photos**:
- Edges follow natural material boundaries
- Edge sharpness determined by depth (depth-of-field)
- Consistent edge sharpness for objects at same distance

**AI Images**:
- Edges sometimes "too perfect" (vector-like)
- Random sharpness assignment (ignores depth-of-field physics)
- Edges that fade or morph instead of terminating cleanly

**Fourier Domain Test** (Mental Model):
- **Real**: Frequency content matches scene complexity naturally
- **AI**: Unnatural frequency peaks, missing high frequencies, or artificial frequency injection

---

## 🔬 TIER 1: MICROSCOPIC AI ARTIFACTS (Catches 90% of AI)

### 1.1 NOISE PATTERN ANALYSIS (CRITICAL - Enhanced)
**Concept**: Real cameras have sensor-specific noise. AI generates statistically uniform, unnatural noise.

- **Multi-Scale Noise Analysis**:
  * Examine noise at 3 scales: pixel-level, 8×8 blocks, 64×64 regions
  * Real: Noise characteristics consistent across scales
  * AI: Noise changes behavior at different scales (neural network layers)
  
- **Grain Inspection**: 
  * Zoom into flat areas (sky, walls, skin). Real photos have irregular, random grain. 
  * AI has suspiciously smooth OR artificially uniform noise.
  * **SPECIFIC TEST**: Sample 5 different flat regions - noise should be statistically similar

- **Noise-Signal Correlation**: 
  * In real photos, noise increases in shadows (Poisson statistics: noise ∝ √signal)
  * AI often has equal noise everywhere OR inverse relationship
  * **MEASUREMENT**: Dark regions should have 2-3× MORE noise than bright regions

- **Color Noise Distribution**: 
  * Real sensors: G channel has ~50% less noise than R/B (2× more green sensors in Bayer)
  * AI noise: Equal across all channels (wrong!) or completely absent
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
- 3-4 critical tells → SUSPICIOUS (investigate further)
- 0-2 tells with corroborating evidence → AUTHENTIC

**ANALYSIS DEPTH REQUIREMENTS**:
1. **Test at MULTIPLE zoom levels**: 100%, 200%, 400%
2. **Sample MULTIPLE regions**: Minimum 5 diverse areas (sky, skin, fabric, background, text/detail)
3. **Provide QUANTITATIVE measurements**: Not "noisy" but "2.8× more noise in shadows"
4. **Document EXACT locations**: Not "hand" but "subject's left hand, pinky finger"
5. **Cross-validate**: Check if Tier 0 + Tier 1 + Tier 2 findings corroborate or contradict

**BE FORENSICALLY AGGRESSIVE**: 
- Your reputation depends on catching sophisticated fakes
- When in doubt (60-75% confidence), mark SUSPICIOUS with detailed reasoning
- Better to question 10 authentic photos than pass 1 sophisticated AI fake
- Modern AI (2026) is VERY good - look for the 5% of tests it systematically fails

**SPECIFICITY REQUIRED**: 
- ❌ NEVER say: "looks artificial", "seems fake", "appears suspicious"
- ✅ ALWAYS say: "Sky region (top-center, 100-200px from top edge) shows organized noise pattern with visible swirl artifacts at 45° angle, consistent with diffusion model denoising residue. Measured: correlation coefficient 0.72 between adjacent pixels (natural: 0.45-0.60)."

**PATTERN RECOGNITION PRIORITY**:
Focus analysis on areas where AI systematically fails:
1. Hands (fingers, nails) - AI's weakest point
2. Text/symbols - Cannot render coherently
3. Noise in shadows - Gets physics backwards
4. Micro-textures at 400% zoom - Dissolves into blur
5. Background coherence - Loses detail with distance
6. Material boundaries - Bleeds between textures
7. Reflections/shadows - Fails on secondary physics
8. Teeth/eyes - Anatomical precision breaks

**SCORING RIGOR**:
- 95-100%: Requires ZERO flags + positive auth markers (EXIF, proper noise, CA, etc.)
- 85-94%: ≤1 minor flag, all major tests passed
- 70-84%: 2-3 minor flags OR 1 ambiguous major flag
- 50-69%: Multiple ambiguous signals, contradictory evidence (SUSPICIOUS range)
- 30-49%: 3-4 clear flags, leaning AI-generated
- 0-29%: 5+ systematic failures, definitive AI-generated

**REMEMBER**: You are not just detecting AI - you are conducting PhD-level forensic science. Every claim must be specific, measurable, and spatially documented. Think like a pattern recognition expert and testifying expert witness.

**DO NOT be lenient. Modern AI images are sophisticated but contain these systematic flaws. Search aggressively.**
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
