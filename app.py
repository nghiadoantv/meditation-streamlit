import streamlit as st
from database import *

# Khởi tạo database
init_db()

# Session state cho login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

# Trang login/register
if not st.session_state.logged_in:
    st.title("🧘 Đăng Nhập / Đăng Ký")
    
    tab1, tab2 = st.tabs(["Đăng Nhập", "Đăng Ký"])
    
    with tab1:
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Đăng Nhập"):
            user_id = login_user(login_username, login_password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = login_username
                st.rerun()
            else:
                st.error("Sai username hoặc password!")
    
    with tab2:
        reg_username = st.text_input("Username", key="reg_user")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        reg_password2 = st.text_input("Xác nhận Password", type="password")
        
        if st.button("Đăng Ký"):
            if reg_password != reg_password2:
                st.error("Password không khớp!")
            elif register_user(reg_username, reg_password):
                st.success("Đăng ký thành công! Hãy đăng nhập.")
            else:
                st.error("Username đã tồn tại!")
    
    st.stop()

# Sidebar với thông tin user
with st.sidebar:
    st.write(f"👤 Xin chào **{st.session_state.username}**")
    
    # Hiển thị streak
    streak = calculate_streak(st.session_state.user_id)
    total_days = get_total_days(st.session_state.user_id)
    stats = get_user_stats(st.session_state.user_id)
    
    st.metric("🔥 Streak hiện tại", f"{streak} ngày")
    st.metric("📅 Tổng số ngày", f"{total_days} ngày")
    st.metric("⏱️ Tổng thời gian", f"{stats['total_minutes']} phút")
    
    if st.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()

# Sau khi hoàn thành thiền, lưu session
# Thêm vào phần completeMeditation trong HTML:
"""
// Gọi API để lưu session (cần thêm endpoint)
fetch('/save_session', {
    method: 'POST',
    body: JSON.stringify({
        user_id: USER_ID,
        cycles: currentCycle,
        duration: DURATION
    })
})
"""
