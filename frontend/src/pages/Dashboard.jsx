import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const Dashboard = () => {
  // ===== STATE =====
  const { user, logout } = useAuth();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' });

  // ===== TOAST =====
  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type });
    setTimeout(() => {
      setToast({ show: false, message: '', type: 'success' });
    }, 3000);
  };

  // ===== GENERATE POSTS =====
  const generatePosts = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/posts/generate-posts', {
        days: 30,
        categories: ['product', 'lifestyle', 'tips'],
        platforms: ['facebook', 'instagram', 'linkedin']
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setPosts(response.data.posts);
      showToast('✅ 30 posts generated successfully!');
    } catch (error) {
      console.error('Error generating posts:', error);
      showToast('❌ Failed to generate posts. Please try again.', 'error');
    }
    setLoading(false);
  };

  // ===== EXPORT JSON =====
  const exportPosts = () => {
    if (posts.length === 0) {
      showToast('⚠️ No posts to export. Generate posts first!', 'error');
      return;
    }
    const data = posts.map(post => ({
      day: post.day,
      category: post.category,
      title: post.title,
      preview: post.preview,
      time: post.time,
      platforms: post.platforms.join(', '),
      likes: post.likes,
      comments: post.comments,
      shares: post.shares
    }));
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `posts_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('📥 Posts exported successfully!');
  };

  // ===== EXPORT CSV =====
  const exportCSV = () => {
    if (posts.length === 0) {
      showToast('⚠️ No posts to export. Generate posts first!', 'error');
      return;
    }
    const headers = ['Day', 'Category', 'Title', 'Preview', 'Time', 'Platforms', 'Likes', 'Comments', 'Shares'];
    const rows = posts.map(post => [
      post.day,
      post.category,
      `"${post.title}"`,
      `"${post.preview}"`,
      post.time,
      post.platforms.join('; '),
      post.likes,
      post.comments,
      post.shares
    ]);
    const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `posts_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('📊 CSV exported successfully!');
  };

  // ===== COPY POSTS =====
  const copyPosts = () => {
    if (posts.length === 0) {
      showToast('⚠️ No posts to copy. Generate posts first!', 'error');
      return;
    }
    const text = posts.map(post => 
      `Day ${post.day} - ${post.category}\n${post.title}\n${post.preview}\n${post.time}\n❤️ ${post.likes} 💬 ${post.comments} 🔄 ${post.shares}\n---`
    ).join('\n');
    navigator.clipboard.writeText(text);
    showToast('📋 Posts copied to clipboard!');
  };

  // ===== CLEAR POSTS =====
  const clearPosts = () => {
    if (posts.length === 0) return;
    if (window.confirm('Are you sure you want to delete all posts?')) {
      setPosts([]);
      showToast('🗑️ All posts cleared!');
    }
  };

  // ===== GET STATS =====
  const getStats = () => {
    if (posts.length === 0) return null;
    const totalLikes = posts.reduce((sum, p) => sum + p.likes, 0);
    const totalComments = posts.reduce((sum, p) => sum + p.comments, 0);
    const totalShares = posts.reduce((sum, p) => sum + p.shares, 0);
    return { totalLikes, totalComments, totalShares, total: posts.length };
  };

  const stats = getStats();
  const filteredPosts = filter === 'all' 
    ? posts 
    : posts.filter(post => post.category.toLowerCase() === filter);

  // ===== RENDER =====
  return (
    <div className="dashboard-container">
      {/* Toast */}
      {toast.show && (
        <div className={`toast ${toast.show ? 'show' : ''}`} style={{
          background: toast.type === 'error' ? '#dc2626' : toast.type === 'warning' ? '#d97706' : '#0f172a'
        }}>
          <i className={`fas ${toast.type === 'error' ? 'fa-exclamation-circle' : toast.type === 'warning' ? 'fa-exclamation-triangle' : 'fa-check-circle'}`}></i>
          {toast.message}
        </div>
      )}

      {/* Header */}
      <header className="header">
        <div className="user-info">
          <i className="fas fa-user-circle"></i>
          <span>{user?.name || user?.email}</span>
        </div>
        <button className="logout-btn" onClick={logout}>
          <i className="fas fa-sign-out-alt"></i> Logout
        </button>
      </header>

      {/* Stats Cards */}
      {stats && (
        <div className="stats-container">
          <div className="stat-card">
            <div className="stat-icon">📝</div>
            <div className="stat-info">
              <span className="stat-value">{stats.total}</span>
              <span className="stat-label">Total Posts</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">❤️</div>
            <div className="stat-info">
              <span className="stat-value">{stats.totalLikes}</span>
              <span className="stat-label">Total Likes</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">💬</div>
            <div className="stat-info">
              <span className="stat-value">{stats.totalComments}</span>
              <span className="stat-label">Total Comments</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔄</div>
            <div className="stat-info">
              <span className="stat-value">{stats.totalShares}</span>
              <span className="stat-label">Total Shares</span>
            </div>
          </div>
        </div>
      )}

      {/* Generator Card */}
      <section className="generator-card">
        <h2>Generate 30 Days of Content</h2>
        <p className="subhead">e.g. product, lifestyle, tips</p>

        <div className="options-row">
          <div className="option-tag">
            <i className="fas fa-tag"></i>
            <span>Product</span> <small>·</small> 
            <span>Lifestyle</span> <small>·</small> 
            <span>Tips</span>
          </div>
          <div className="platform-icons">
            <i className="fab fa-facebook"></i>
            <i className="fab fa-instagram"></i>
            <i className="fab fa-linkedin"></i>
          </div>
        </div>

        <div className="btn-wrapper">
          <button 
            className="generate-btn" 
            onClick={generatePosts}
            disabled={loading}
          >
            <i className={`fas ${loading ? 'fa-spinner fa-spin' : 'fa-magic'}`}></i>
            {loading ? 'Generating...' : 'Generate Posts'}
          </button>
          
          {posts.length > 0 && (
            <div className="export-btn-group">
              <button className="export-btn" onClick={exportPosts} title="Export as JSON">
                <i className="fas fa-file-export"></i> JSON
              </button>
              <button className="export-btn" onClick={exportCSV} title="Export as CSV">
                <i className="fas fa-file-csv"></i> CSV
              </button>
              <button className="export-btn" onClick={copyPosts} title="Copy to clipboard">
                <i className="fas fa-copy"></i> Copy
              </button>
              <button className="export-btn" onClick={clearPosts} title="Clear all posts" style={{ color: '#dc2626' }}>
                <i className="fas fa-trash"></i> Clear
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Posts Section */}
      <div className="posts-header">
        <h3>Your Posts <span>· {posts.length} days</span></h3>
        <span><i className="far fa-calendar-alt"></i> Day 1 – {posts.length}</span>
      </div>

      {/* Filters */}
      <div className="filter-buttons">
        {['all', 'product', 'lifestyle', 'tips'].map(cat => (
          <button
            key={cat}
            className={`filter-btn ${filter === cat ? 'active' : ''}`}
            onClick={() => setFilter(cat)}
          >
            {cat === 'all' ? 'All' : cat.charAt(0).toUpperCase() + cat.slice(1)}
            {cat !== 'all' && (
              <span className="filter-count">
                {posts.filter(p => p.category.toLowerCase() === cat).length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Posts Grid */}
      <div className="posts-grid">
        {posts.length === 0 ? (
          <div className="empty-state">
            <i className="fas fa-newspaper"></i>
            <p>No posts yet. Click "Generate Posts" to create 30 days of content!</p>
          </div>
        ) : filteredPosts.length === 0 ? (
          <div className="empty-state">
            <i className="fas fa-filter"></i>
            <p>No posts found for "{filter}" category.</p>
          </div>
        ) : (
          filteredPosts.map((post) => (
            <div key={post.day} className="post-card" data-category={post.category.toLowerCase()}>
              <span className="post-badge" style={{
                background: post.category === 'Product' ? '#dbeafe' : 
                           post.category === 'Lifestyle' ? '#d1fae5' : '#fef3c7',
                color: post.category === 'Product' ? '#1e40af' : 
                       post.category === 'Lifestyle' ? '#065f46' : '#92400e'
              }}>
                {post.category} · Day {post.day}
              </span>
              <div className="post-title">{post.title}</div>
              <div className="post-preview">{post.preview}</div>
              <div className="post-meta">
                <span><i className="far fa-clock"></i> {post.time}</span>
                <div className="post-platforms">
                  {post.platforms.map(p => (
                    <i key={p} className={`fab fa-${p}`}></i>
                  ))}
                </div>
              </div>
              <div className="post-engagement">
                <span>❤️ {post.likes}</span>
                <span>💬 {post.comments}</span>
                <span><i className="fas fa-share-alt"></i> {post.shares}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;