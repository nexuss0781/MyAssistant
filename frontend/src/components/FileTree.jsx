import React, { useState, useEffect } from 'react';

const FileTree = ({ sessionId, onFileSelect }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!sessionId) return;

    const fetchFiles = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:8000/sessions/${sessionId}/files?path=.`);
        if (!response.ok) throw new Error('Failed to fetch file tree');
        const data = await response.json();
        if (data.status === 'error') {
          throw new Error(data.message);
        }
        setFiles(data.contents);
      } catch (err) {
        setError(`Failed to load file tree: ${err.message}`);
        console.error('Error fetching file tree:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [sessionId]);

  const renderFile = (file) => (
    <div key={file.path} style={{ marginLeft: file.path.split('/').length * 10 }}>
      {file.type === 'folder' ? (
        <span className="folder-icon">📁 {file.name}</span>
      ) : (
        <span className="file-icon" onClick={() => onFileSelect(file.path)} style={{ cursor: 'pointer' }}>📄 {file.name}</span>
      )}
    </div>
  );

  if (loading) return <p>Loading files...</p>;
  if (error) return <p className="text-danger">Error: {error}</p>;

  return (
    <div className="file-tree">
      {files.map(renderFile)}
    </div>
  );
};

export default FileTree;

