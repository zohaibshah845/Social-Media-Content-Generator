import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { generateContent, listPosts, createGraphic, schedulePost } from '../api/api';
import { useNavigate } from 'react-router-dom';

const styles = {
  dashboard: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '2px solid #eee',
    paddingBottom: '15px',
    marginBottom: '25px',
  },
  logoutButton: {
    padding: '8px 16px',
    backgroundColor: '#dc3545',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'background 0.2s',
  },
  panel: {
    background: '#f8f9fa',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '30px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
  },
  panelTitle: {
    marginTop: 0,
    marginBottom: '15px',
    color: '#333',
  },
  input: {
    padding: '10px',
    marginRight: '10px',
    marginBottom: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    flex: 1,
    minWidth: '200px',
  },
  select: {
    padding: '10px',
    marginRight: '10px',
    marginBottom: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
    minHeight: '80px',
    minWidth: '150px',
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'background 0.2s',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  postsContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '20px',
  },
  postCard: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '15px',
    background: '#fff',
    boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
    transition: 'box-shadow 0.2s',
  },
  postCaption: {
    fontWeight: 'bold',
    fontSize: '16px',
    marginBottom: '8px',
  },
  postMeta: {
    fontSize: '14px',
    color: '#555',
    marginBottom: '8px',
  },
  postImage: {
    maxWidth: '100%',
    height: 'auto',
    borderRadius: '4px',
    marginBottom: '10px',
  },
  graphicButton: {
    padding: '6px 12px',
    backgroundColor: '#6c757d',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    marginBottom: '10px',
    transition: 'background 0.2s',
  },
  scheduleRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginTop: '10px',
  },
  scheduleInput: {
    padding: '6px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '13px',
    flex: 1,
  },
  scheduleButton: {
    padding: '6px 12px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    transition: 'background 0.2s',
  },
  status: {
    marginTop: '10px',
    fontSize: '13px',
    color: '#666',
    fontStyle: 'italic',
  },
};

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [themes, setThemes] = useState('');
  const [platforms, setPlatforms] = useState(['facebook', 'instagram', 'linkedin']);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) navigate('/login');
    else fetchPosts();
  }, [user, navigate]);

  const fetchPosts = async () => {
    try {
      const res = await listPosts();
      setPosts(res.data.posts);
    } catch (err) { console.error(err); }
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const themesArray = themes.split(',').map(t => t.trim());
      const res = await generateContent({ themes: themesArray, platforms, count: 30 });
      setPosts(res.data.posts);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const handleGraphic = async (postId) => {
    try {
      await createGraphic(postId);
      fetchPosts();
    } catch (err) { console.error(err); }
  };

  const handleSchedule = async (postId, scheduledTime) => {
    try {
      await schedulePost({ post_id: postId, platforms, scheduled_time: scheduledTime });
      fetchPosts();
    } catch (err) { console.error(err); }
  };

  return (
    <div style={styles.dashboard}>
      <div style={styles.header}>
        <h2>📊 Dashboard – {user?.email}</h2>
        <button style={styles.logoutButton} onClick={logout}>Logout</button>
      </div>

      <div style={styles.panel}>
        <h3 style={styles.panelTitle}>Generate 30 Days of Content</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'flex-start' }}>
          <input
            style={styles.input}
            value={themes}
            onChange={(e) => setThemes(e.target.value)}
            placeholder="e.g. product, lifestyle, tips"
          />
          <select
            style={styles.select}
            multiple
            value={platforms}
            onChange={(e) => setPlatforms([...e.target.selectedOptions].map(o => o.value))}
          >
            <option value="facebook">Facebook</option>
            <option value="instagram">Instagram</option>
            <option value="linkedin">LinkedIn</option>
          </select>
          <button
            style={{ ...styles.button, ...(loading ? styles.buttonDisabled : {}) }}
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Posts'}
          </button>
        </div>
      </div>

      <div>
        <h3>Your Posts</h3>
        <div style={styles.postsContainer}>
          {posts.map(p => (
            <div key={p.id} style={styles.postCard}>
              <p style={styles.postCaption}>{p.caption}</p>
              <p style={styles.postMeta}># {p.hashtags?.join(' #')}</p>
              <p style={styles.postMeta}>Category: {p.category}</p>
              {p.image_url ? (
                <img src={p.image_url} alt="post visual" style={styles.postImage} />
              ) : (
                <button style={styles.graphicButton} onClick={() => handleGraphic(p.id)}>
                  Generate Graphic
                </button>
              )}
              <div style={styles.scheduleRow}>
                <input
                  type="datetime-local"
                  style={styles.scheduleInput}
                  onChange={(e) => { p.scheduledTime = e.target.value; }}
                />
                <button
                  style={styles.scheduleButton}
                  onClick={() => handleSchedule(p.id, p.scheduledTime)}
                >
                  Schedule
                </button>
              </div>
              <p style={styles.status}>Status: {p.status}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}