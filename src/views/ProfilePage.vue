// 处理头像变更
const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请上传图片文件')
    return
  }
  
  // 验证文件大小
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    return
  }
  
  try {
    // 显示上传中提示
    alert('头像上传中，请稍候...')
    
    // 使用原生fetch API上传
    const formData = new FormData()
    formData.append('avatar', file)
    
    // 确保从userData中获取用户ID
    const userId = userStore.state.userData?.id || '1'
    console.log('上传头像，用户ID:', userId)
    console.log('使用的Token:', userStore.state.token)
    
    // 使用完整的URL，不使用相对路径
    const response = await fetch(`http://localhost:5000/api/auth/avatar/${userId}`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${userStore.state.token}`
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.message || `上传失败: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('上传响应:', data)
    
    if (data.success) {
      console.log('头像上传成功，URL:', data.data.avatar_url)
      userStore.updateAvatar(data.data.avatar_url)
      console.log('更新后的头像URL:', userStore.state.avatar)
      alert('头像更新成功')
    } else {
      throw new Error(data.message || '头像上传失败')
    }
  } catch (error) {
    console.error('上传头像失败:', error)
    alert('头像上传失败: ' + error.message)
  }
} 