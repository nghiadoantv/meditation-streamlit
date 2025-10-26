import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import base64
import os


# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Thiền Hơi Thở",
    page_icon="🧘",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==================== CSS ====================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE ====================
if 'audio_generated' not in st.session_state:
    st.session_state.audio_generated = False


# ==================== FUNCTIONS ====================
def generate_audio_file(text, filename):
    """Tạo file audio từ text bằng gTTS"""
    audio_dir = "audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    filepath = os.path.join(audio_dir, filename)
    
    if not os.path.exists(filepath):
        try:
            tts = gTTS(text=text, lang='vi', slow=False)
            tts.save(filepath)
            return True
        except Exception as e:
            st.error(f"Lỗi tạo audio: {e}")
            return False
    return True


def get_audio_base64(file_path):
    """Chuyển audio thành base64"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except:
        return None


def pregenerate_audio_files():
    """Tạo sẵn tất cả file audio cần thiết"""
    audio_texts = {
        "prepare.mp3": "Hãy ngồi thoải mái và chuẩn bị tinh thần",
        "ready.mp3": "Chuẩn bị bắt đầu",
        "inhale.mp3": "Hít vào",
        "hold.mp3": "Giữ hơi",
        "exhale.mp3": "Thở ra",
        "complete.mp3": "Hoàn thành. Chúc mừng bạn",
        # Countdown numbers - CHỈ dùng cho giai đoạn chuẩn bị
        "countdown_10.mp3": "10",
        "countdown_9.mp3": "9",
        "countdown_8.mp3": "8",
        "countdown_7.mp3": "7",
        "countdown_6.mp3": "6",
        "countdown_5.mp3": "5",
        "countdown_4.mp3": "4",
        "countdown_3.mp3": "3",
        "countdown_2.mp3": "2",
        "countdown_1.mp3": "1"
    }
    
    with st.spinner("🎵 Đang chuẩn bị giọng nói..."):
        for filename, text in audio_texts.items():
            generate_audio_file(text, filename)
    
    st.session_state.audio_generated = True


# ==================== GIAO DIỆN CHÍNH ====================
st.title("🧘 Thiền Hơi Thở Cho Người Mới")
st.markdown("### _Hướng dẫn hơi thở có giọng nói tiếng Việt_")


# ==================== CÀI ĐẶT ====================
st.markdown("---")
st.subheader("⚙️ Cài Đặt")

col1, col2 = st.columns(2)

with col1:
    prepare_time = st.number_input(
        "⏱️ Chuẩn bị (giây)",
        min_value=3,
        max_value=30,
        value=10,
        step=1,
        help="Thời gian chuẩn bị tinh thần trước khi bắt đầu thiền"
    )

with col2:
    infinite_mode = st.checkbox(
        "♾️ Chế độ vô hạn",
        value=False,
        help="Thiền không giới hạn số chu kỳ - dừng khi muốn"
    )

if not infinite_mode:
    total_cycles = st.number_input(
        "🔄 Số chu kỳ",
        min_value=1,
        max_value=999,
        value=10,
        step=1,
        help="Số chu kỳ hít vào - giữ hơi - thở ra"
    )
else:
    total_cycles = 0  # 0 = infinite
    st.info("♾️ Chế độ vô hạn: Thiền sẽ tiếp tục cho đến khi bạn nhấn Dừng")

st.markdown("#### 🌬️ Thời gian hơi thở")
col3, col4, col5 = st.columns(3)

with col3:
    inhale_time = st.number_input(
        "🌬️ Hít vào (giây)",
        min_value=2,
        max_value=10,
        value=4,
        step=1
    )

with col4:
    hold_time = st.number_input(
        "⏸️ Giữ hơi (giây)",
        min_value=0,
        max_value=10,
        value=4,
        step=1,
        help="Thời gian giữ hơi sau khi hít vào (có thể để 0 để bỏ qua)"
    )

with col5:
    exhale_time = st.number_input(
        "💨 Thở ra (giây)",
        min_value=2,
        max_value=10,
        value=6,
        step=1
    )

# Hiển thị tổng thời gian 1 chu kỳ
cycle_duration = inhale_time + hold_time + exhale_time
st.info(f"⏱️ Tổng thời gian 1 chu kỳ: **{cycle_duration} giây** (Hít: {inhale_time}s + Giữ: {hold_time}s + Thở: {exhale_time}s)")


# ==================== TÙY CHỌN GIỌNG ĐỌC ====================
st.markdown("---")
st.subheader("🗣️ Tùy Chọn Giọng Đọc")

prepare_countdown_voice = st.checkbox(
    "⏱️ Đọc số đếm ngược chuẩn bị",
    value=True,
    help="Giọng đọc sẽ đọc số khi đếm ngược giai đoạn chuẩn bị (10, 9, 8...)"
)

st.info("ℹ️ **Trong lúc thiền**: Chỉ đọc 'Hít vào', 'Giữ hơi' và 'Thở ra' - KHÔNG đọc số đếm giây")


# ==================== ÂM LƯỢNG ====================
st.markdown("---")
st.subheader("🔊 Âm Lượng")

col_v1, col_v2 = st.columns(2)

with col_v1:
    voice_volume = st.slider(
        "🗣️ Giọng đọc",
        min_value=0,
        max_value=100,
        value=80,
        step=5
    ) / 100

with col_v2:
    music_volume = st.slider(
        "🎵 Nhạc nền",
        min_value=0,
        max_value=100,
        value=30,
        step=5
    ) / 100


# ==================== NHẠC NỀN ====================
st.markdown("---")

# Check if music file exists and get base64
music_b64 = None
if os.path.exists("meditation_music.mp3"):
    st.success("✅ Nhạc nền đã sẵn sàng - sẽ tự động phát khi bắt đầu thiền")
    music_b64 = get_audio_base64("meditation_music.mp3")
    if not music_b64:
        st.warning("⚠️ File nhạc quá lớn, không thể tự động phát. Dùng audio player thủ công bên dưới:")
        st.audio("meditation_music.mp3", format="audio/mp3")
else:
    st.warning("⚠️ Chưa có file nhạc nền. Upload file MP3 bên dưới.")


# ==================== CHUẨN BỊ AUDIO ====================
if not st.session_state.audio_generated:
    if st.button("🎙️ Chuẩn Bị Giọng Nói", type="primary", use_container_width=True):
        pregenerate_audio_files()
        st.success("✅ Đã tạo xong file giọng nói!")
        st.rerun()
else:
    # Load audio base64
    prepare_b64 = get_audio_base64("audio/prepare.mp3")
    ready_b64 = get_audio_base64("audio/ready.mp3")
    inhale_b64 = get_audio_base64("audio/inhale.mp3")
    hold_b64 = get_audio_base64("audio/hold.mp3")
    exhale_b64 = get_audio_base64("audio/exhale.mp3")
    complete_b64 = get_audio_base64("audio/complete.mp3")
    
    # Load countdown audio
    countdown_audios = {}
    for i in range(1, 11):
        audio_b64 = get_audio_base64(f"audio/countdown_{i}.mp3")
        if audio_b64:
            countdown_audios[i] = audio_b64
    
    # ==================== APP THIỀN (HTML COMPONENT) ====================
    st.markdown("---")
    
    # Convert countdown audios to JavaScript object
    countdown_js = "{\n"
    for num, b64 in countdown_audios.items():
        countdown_js += f'        {num}: "data:audio/mp3;base64,{b64}",\n'
    countdown_js += "    }"
    
    meditation_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
            }}
            
            .big-status {{
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                padding: 40px;
                border-radius: 20px;
                margin: 20px 0;
                animation: pulse 2s ease-in-out infinite;
            }}
            
            .prepare {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            .inhale {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            .hold {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }}
            
            .exhale {{ 
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
            }}
            
            .complete {{
                background: linear-gradient(135deg, #fad961 0%, #f76b1c 100%);
                color: white;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
            
            .countdown-timer {{
                font-size: 72px;
                font-weight: bold;
                margin-top: 20px;
                animation: countdown-pulse 1s ease-in-out infinite;
            }}
            
            @keyframes countdown-pulse {{
                0%, 100% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.1); opacity: 0.8; }}
            }}
            
            .cycle-info {{
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                background: #f0f2f6;
                border-radius: 10px;
                margin: 10px 0;
            }}
            
            button {{
                width: 48%;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin: 5px;
            }}
            
            .start-btn {{
                background: #27ae60;
                color: white;
            }}
            
            .stop-btn {{
                background: #e74c3c;
                color: white;
            }}
            
            button:hover {{
                opacity: 0.9;
            }}
            
            button:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            progress {{
                width: 100%;
                height: 30px;
                border-radius: 10px;
            }}
            
            .infinite-symbol {{
                font-size: 40px;
                animation: rotate 3s linear infinite;
            }}
            
            @keyframes rotate {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div id="status-display"></div>
        <div id="cycle-display"></div>
        <div id="progress-display"></div>
        
        <div style="text-align: center; margin-top: 20px;">
            <button class="start-btn" id="startBtn" onclick="startMeditation()">▶️ Bắt Đầu</button>
            <button class="stop-btn" id="stopBtn" onclick="stopMeditation()">⏹️ Dừng</button>
        </div>
        
        <script>
            // Audio files (voice)
            const audios = {{
                prepare: "data:audio/mp3;base64,{prepare_b64}",
                ready: "data:audio/mp3;base64,{ready_b64}",
                inhale: "data:audio/mp3;base64,{inhale_b64}",
                hold: "data:audio/mp3;base64,{hold_b64}",
                exhale: "data:audio/mp3;base64,{exhale_b64}",
                complete: "data:audio/mp3;base64,{complete_b64}"
            }};
            
            // Countdown numbers audio - CHỈ dùng cho giai đoạn chuẩn bị
            const countdownAudios = {countdown_js};
            
            // Background music
            const bgMusicData = {"'data:audio/mp3;base64," + music_b64 + "'" if music_b64 else "null"};
            let bgMusic = null;
            
            // Settings
            const settings = {{
                prepareTime: {prepare_time},
                inhaleTime: {inhale_time},
                holdTime: {hold_time},
                exhaleTime: {exhale_time},
                totalCycles: {total_cycles},  // 0 = infinite
                voiceVolume: {voice_volume},
                musicVolume: {music_volume},
                prepareCountdownVoice: {"true" if prepare_countdown_voice else "false"}
            }};
            
            const isInfiniteMode = settings.totalCycles === 0;
            
            // State
            let currentCycle = 0;
            let currentPhase = 'idle';
            let countdown = 0;
            let intervalId = null;
            
            // Initialize background music
            if (bgMusicData) {{
                bgMusic = new Audio(bgMusicData);
                bgMusic.loop = true;
                bgMusic.volume = settings.musicVolume;
            }}
            
            // Play audio
            function playAudio(type) {{
                const audio = new Audio(audios[type]);
                audio.volume = settings.voiceVolume;
                audio.play().catch(e => console.log('Audio play prevented:', e));
            }}
            
            // Play countdown number - CHỈ cho giai đoạn chuẩn bị
            function playCountdownNumber(number) {{
                if (countdownAudios[number]) {{
                    const audio = new Audio(countdownAudios[number]);
                    audio.volume = settings.voiceVolume;
                    audio.play().catch(e => console.log('Countdown audio play prevented:', e));
                }}
            }}
            
            // Play background music
            function playBgMusic() {{
                if (bgMusic) {{
                    bgMusic.currentTime = 0;
                    bgMusic.play().catch(e => console.log('BG music play prevented:', e));
                }}
            }}
            
            // Stop background music
            function stopBgMusic() {{
                if (bgMusic) {{
                    bgMusic.pause();
                    bgMusic.currentTime = 0;
                }}
            }}
            
            // Update display
            function updateDisplay(status, cycle, progress) {{
                document.getElementById('status-display').innerHTML = status;
                document.getElementById('cycle-display').innerHTML = cycle || '';
                document.getElementById('progress-display').innerHTML = progress || '';
            }}
            
            // Countdown function - CHỈ đọc số trong giai đoạn chuẩn bị
            function runCountdown(seconds, callback, enableVoice = false) {{
                countdown = seconds;
                
                if (intervalId) clearInterval(intervalId);
                
                intervalId = setInterval(() => {{
                    if (currentPhase === 'idle') {{
                        clearInterval(intervalId);
                        return;
                    }}
                    
                    countdown--;
                    
                    // CHỈ đọc số khi enableVoice = true (giai đoạn chuẩn bị)
                    if (enableVoice && countdown >= 1 && countdown <= 10) {{
                        playCountdownNumber(countdown);
                    }}
                    
                    // Update countdown display
                    const statusDiv = document.getElementById('status-display');
                    if (statusDiv) {{
                        const timerSpan = statusDiv.querySelector('.countdown-timer');
                        if (timerSpan) timerSpan.textContent = countdown;
                    }}
                    
                    if (countdown <= 0) {{
                        clearInterval(intervalId);
                        callback();
                    }}
                }}, 1000);
            }}
            
            // Start meditation
            function startMeditation() {{
                console.log('Starting meditation preparation...');
                
                // Disable start button
                document.getElementById('startBtn').disabled = true;
                
                currentPhase = 'prepare';
                currentCycle = 0;
                
                // Show preparation phase
                updateDisplay(
                    '<div class="big-status prepare">Chuẩn Bị Tinh Thần 🧘<div class="countdown-timer">' + settings.prepareTime + '</div></div>',
                    '<div class="cycle-info">Hãy ngồi thoải mái và thư giãn...</div>',
                    ''
                );
                
                playAudio('prepare');
                
                // Run preparation countdown WITH voice (đọc số 10, 9, 8...)
                runCountdown(settings.prepareTime, () => {{
                    // Play "ready" sound
                    playAudio('ready');
                    
                    // Show "Chuẩn bị bắt đầu..." và ĐỢI 2 GIÂY
                    updateDisplay(
                        '<div class="big-status prepare">Chuẩn Bị Bắt Đầu... 🌟</div>',
                        '<div class="cycle-info">Đang khởi động nhạc nền...</div>',
                        ''
                    );
                    
                    // Start background music
                    playBgMusic();
                    
                    // ĐỢI 2 GIÂY trước khi bắt đầu thiền
                    setTimeout(() => {{
                        breathingCycle();
                    }}, 2000);
                }}, settings.prepareCountdownVoice);
            }}
            
            // Breathing cycle - KHÔNG đọc số, chỉ hiển thị và đọc "Hít vào"/"Giữ hơi"/"Thở ra"
            function breathingCycle() {{
                if (currentPhase === 'idle') return;
                
                currentCycle++;
                
                // Check if we should stop (only for non-infinite mode)
                if (!isInfiniteMode && currentCycle > settings.totalCycles) {{
                    completeMeditation();
                    return;
                }}
                
                // Prepare cycle display text
                let cycleText = '';
                if (isInfiniteMode) {{
                    cycleText = '<div class="cycle-info">Chu kỳ: ' + currentCycle + ' <span class="infinite-symbol">♾️</span></div>';
                }} else {{
                    cycleText = '<div class="cycle-info">Chu kỳ: ' + currentCycle + '/' + settings.totalCycles + '</div>';
                }}
                
                // Prepare progress bar
                let progressBar = '';
                if (isInfiniteMode) {{
                    progressBar = '<div style="text-align:center; font-size:40px;">♾️</div>';
                }} else {{
                    progressBar = '<progress value="' + currentCycle + '" max="' + settings.totalCycles + '"></progress>';
                }}
                
                // Inhale phase - HIỂN THỊ số giây nhưng KHÔNG ĐỌC
                currentPhase = 'inhale';
                
                updateDisplay(
                    '<div class="big-status inhale">HÍT VÀO 🌬️<div class="countdown-timer">' + settings.inhaleTime + '</div></div>',
                    cycleText,
                    progressBar
                );
                
                // CHỈ đọc "Hít vào" - KHÔNG đọc số
                playAudio('inhale');
                
                // runCountdown với enableVoice = FALSE (không đọc số)
                runCountdown(settings.inhaleTime, () => {{
                    // Hold phase - HIỂN THỊ số giây nhưng KHÔNG ĐỌC
                    if (settings.holdTime > 0) {{
                        currentPhase = 'hold';
                        
                        updateDisplay(
                            '<div class="big-status hold">GIỮ HƠI ⏸️<div class="countdown-timer">' + settings.holdTime + '</div></div>',
                            cycleText,
                            progressBar
                        );
                        
                        // CHỈ đọc "Giữ hơi" - KHÔNG đọc số
                        playAudio('hold');
                        
                        // runCountdown với enableVoice = FALSE (không đọc số)
                        runCountdown(settings.holdTime, () => {{
                            exhalePhase(cycleText, progressBar);
                        }}, false);
                    }} else {{
                        // Nếu holdTime = 0, bỏ qua giai đoạn giữ hơi
                        exhalePhase(cycleText, progressBar);
                    }}
                }}, false);
            }}
            
            // Exhale phase function
            function exhalePhase(cycleText, progressBar) {{
                currentPhase = 'exhale';
                
                updateDisplay(
                    '<div class="big-status exhale">THỞ RA 💨<div class="countdown-timer">' + settings.exhaleTime + '</div></div>',
                    cycleText,
                    progressBar
                );
                
                // CHỈ đọc "Thở ra" - KHÔNG đọc số
                playAudio('exhale');
                
                // runCountdown với enableVoice = FALSE (không đọc số)
                runCountdown(settings.exhaleTime, () => {{
                    breathingCycle();
                }}, false);
            }}
            
            // Complete meditation
            function completeMeditation() {{
                currentPhase = 'complete';
                
                updateDisplay(
                    '<div class="big-status complete">Hoàn Thành! 🙏</div>',
                    '<div class="cycle-info">Bạn đã hoàn thành ' + currentCycle + ' chu kỳ thiền</div>',
                    '<progress value="100" max="100"></progress>'
                );
                
                playAudio('complete');
                
                // Fade out background music
                if (bgMusic) {{
                    let fadeOutInterval = setInterval(() => {{
                        if (bgMusic.volume > 0.05) {{
                            bgMusic.volume -= 0.05;
                        }} else {{
                            stopBgMusic();
                            clearInterval(fadeOutInterval);
                        }}
                    }}, 200);
                }}
                
                setTimeout(() => {{
                    currentPhase = 'idle';
                    updateDisplay('', '', '');
                    
                    // Reset music volume and re-enable start button
                    if (bgMusic) {{
                        bgMusic.volume = settings.musicVolume;
                    }}
                    document.getElementById('startBtn').disabled = false;
                }}, 3000);
            }}
            
            // Stop meditation
            function stopMeditation() {{
                if (intervalId) clearInterval(intervalId);
                
                // Stop background music immediately
                stopBgMusic();
                
                const cyclesCompleted = currentCycle;
                
                currentPhase = 'idle';
                currentCycle = 0;
                countdown = 0;
                
                let stopMessage = '⏸️ Đã dừng';
                if (cyclesCompleted > 0) {{
                    stopMessage += '<br><small style="font-size:16px;">Bạn đã hoàn thành ' + cyclesCompleted + ' chu kỳ</small>';
                }}
                
                updateDisplay(
                    '<div style="text-align:center; padding:20px; color:#e74c3c; font-size:24px;">' + stopMessage + '</div>',
                    '',
                    ''
                );
                
                setTimeout(() => {{
                    updateDisplay('', '', '');
                    
                    // Reset music volume and re-enable start button
                    if (bgMusic) {{
                        bgMusic.volume = settings.musicVolume;
                    }}
                    document.getElementById('startBtn').disabled = false;
                }}, 3000);
            }}
        </script>
    </body>
    </html>
    """
    
    # Render HTML component
    components.html(meditation_html, height=600, scrolling=False)


# ==================== UPLOAD NHẠC NỀN ====================
st.markdown("---")
with st.expander("🎵 Upload Nhạc Nền"):
    st.info("💡 Upload file nhạc thiền MP3 (khuyến nghị < 20 MB để tự động phát)")
    
    if os.path.exists("meditation_music.mp3"):
        size_mb = os.path.getsize("meditation_music.mp3") / (1024 * 1024)
        if size_mb < 5:
            st.success(f"✅ File hiện tại: {size_mb:.1f} MB - Sẽ tự động phát khi thiền")
        else:
            st.warning(f"⚠️ File hiện tại: {size_mb:.1f} MB - Hơi lớn, khuyến nghị nén xuống < 5 MB")
    
    uploaded_music = st.file_uploader(
        "Chọn file MP3",
        type=['mp3'],
        key='music_uploader'
    )
    
    if uploaded_music:
        file_size = uploaded_music.size / (1024 * 1024)
        
        if file_size > 50:
            st.error(f"❌ File quá lớn ({file_size:.1f} MB). Vui lòng nén xuống < 50 MB")
        else:
            with open("meditation_music.mp3", "wb") as f:
                f.write(uploaded_music.getbuffer())
            st.success(f"✅ Đã lưu nhạc nền ({file_size:.1f} MB)! Refresh trang để áp dụng.")


# ==================== HƯỚNG DẪN NÉN NHẠC ====================
with st.expander("📖 Hướng Dẫn Nén File MP3"):
    st.markdown("""
    ### Cách nén file MP3 xuống < 5 MB (tối ưu cho tự động phát):
    
    **Online Converter (Dễ nhất):**
    - [FreeConvert Audio Compressor](https://www.freeconvert.com/audio-compressor)
    - Upload file → Target: 5 MB → Bitrate: 96 kbps → Convert
    
    **FFmpeg (Nâng cao):**
    ```
    ffmpeg -i input.mp3 -b:a 96k -ac 1 output.mp3
    ```
    
    **Khuyến nghị cho nhạc thiền:**
    - Bitrate: 96 kbps (đủ cho nhạc nền)
    - Mono (1 channel)
    - Độ dài: 10-15 phút (vừa đủ cho 1 session)
    """)


# ==================== KỸ THUẬT THỞ PHỔ BIẾN ====================
with st.expander("🧘 Kỹ Thuật Thở Phổ Biến"):
    st.markdown("""
    ### Các tỷ lệ hơi thở phổ biến:
    
    **Box Breathing (4-4-4-4):**
    - Hít vào: 4 giây
    - Giữ hơi: 4 giây
    - Thở ra: 6 giây
    - Phù hợp cho: Giảm stress, tập trung
    
    **Pranayama (4-7-8):**
    - Hít vào: 4 giây
    - Giữ hơi: 7 giây
    - Thở ra: 8 giây
    - Phù hợp cho: Thư giãn sâu, ngủ ngon
    
    **Wim Hof Basic (deep-0-quick):**
    - Hít vào: 2 giây (sâu)
    - Giữ hơi: 0 giây
    - Thở ra: 2 giây (nhanh)
    - Phù hợp cho: Năng lượng, miễn dịch
    
    **Relaxation (4-0-6):**
    - Hít vào: 4 giây
    - Giữ hơi: 0 giây
    - Thở ra: 6 giây
    - Phù hợp cho: Người mới, thư giãn nhẹ
    """)


# ==================== THÔNG TIN ====================
st.markdown("---")
st.caption("✨ Ứng dụng Thiền Hơi Thở v5.0 | Hít vào - Giữ hơi - Thở ra 🧘")