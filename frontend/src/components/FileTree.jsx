import React, { useState, useEffect } from 'react';

const FileTree = ({ sessionId, onFileSelect }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedFolders, setExpandedFolders] = useState(new Set(['.'])); // Root is expanded by default
  const [fileOperationStatus, setFileOperationStatus] = useState({}); // Track file operation status

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
        
        // Build hierarchical structure
        const fileTree = buildFileTree(data.contents);
        setFiles(fileTree);
      } catch (err) {
        setError(`Failed to load file tree: ${err.message}`);
        console.error('Error fetching file tree:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [sessionId]);

  // Build hierarchical file tree structure
  const buildFileTree = (fileList) => {
    const tree = [];
    const pathMap = {};

    // Sort files so folders come first, then files
    const sortedFiles = fileList.sort((a, b) => {
      if (a.type === 'folder' && b.type !== 'folder') return -1;
      if (a.type !== 'folder' && b.type === 'folder') return 1;
      return a.name.localeCompare(b.name);
    });

    sortedFiles.forEach(file => {
      const pathParts = file.path.split('/').filter(part => part !== '.');
      let currentLevel = tree;
      let currentPath = '';

      pathParts.forEach((part, index) => {
        currentPath = currentPath ? `${currentPath}/${part}` : part;
        
        if (index === pathParts.length - 1) {
          // This is the final part, add the file/folder
          currentLevel.push({
            ...file,
            name: part,
            children: file.type === 'folder' ? [] : undefined,
            depth: pathParts.length - 1
          });
        } else {
          // This is a parent directory, ensure it exists
          let existing = currentLevel.find(item => item.name === part && item.type === 'folder');
          if (!existing) {
            existing = {
              name: part,
              path: currentPath,
              type: 'folder',
              children: [],
              depth: index
            };
            currentLevel.push(existing);
          }
          currentLevel = existing.children;
        }
      });
    });

    return tree;
  };

  const toggleFolder = (folderPath) => {
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(folderPath)) {
        newSet.delete(folderPath);
      } else {
        newSet.add(folderPath);
      }
      return newSet;
    });
  };

  const renderFileNode = (node, depth = 0) => {
    const isExpanded = expandedFolders.has(node.path);
    const hasOperationStatus = fileOperationStatus[node.path];
    const indentStyle = { paddingLeft: `${depth * 20 + 8}px` };

    return (
      <div key={node.path}>
        <div 
          className={`file-tree-item d-flex align-items-center py-1 px-2 ${node.type !== 'folder' ? 'file-item' : 'folder-item'}`}
          style={{ 
            ...indentStyle, 
            cursor: node.type === 'folder' ? 'pointer' : 'default',
            backgroundColor: hasOperationStatus ? '#e3f2fd' : 'transparent',
            borderLeft: hasOperationStatus ? '3px solid #2196f3' : 'none'
          }}
          onClick={() => {
            if (node.type === 'folder') {
              toggleFolder(node.path);
            } else {
              onFileSelect(node.path);
            }
          }}
        >
          {node.type === 'folder' ? (
            <>
              <span className="me-1" style={{ fontSize: '12px' }}>
                {isExpanded ? '📂' : '📁'}
              </span>
              <span className="folder-name">{node.name}</span>
              {hasOperationStatus && (
                <span className="ms-auto text-primary" style={{ fontSize: '12px' }}>
                  {hasOperationStatus}
                </span>
              )}
            </>
          ) : (
            <>
              <span className="me-1" style={{ fontSize: '12px' }}>
                {getFileIcon(node.name)}
              </span>
              <span 
                className="file-name text-primary" 
                style={{ cursor: 'pointer', textDecoration: 'underline' }}
                title="Click to open file"
              >
                {node.name}
              </span>
              {hasOperationStatus && (
                <span className="ms-auto text-success" style={{ fontSize: '12px' }}>
                  {hasOperationStatus}
                </span>
              )}
            </>
          )}
        </div>
        
        {node.type === 'folder' && isExpanded && node.children && (
          <div>
            {node.children.map(child => renderFileNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    const iconMap = {
      'js': '📄',
      'jsx': '⚛️',
      'ts': '📘',
      'tsx': '⚛️',
      'py': '🐍',
      'html': '🌐',
      'css': '🎨',
      'json': '📋',
      'md': '📝',
      'txt': '📄',
      'yml': '⚙️',
      'yaml': '⚙️',
      'xml': '📄',
      'svg': '🖼️',
      'png': '🖼️',
      'jpg': '🖼️',
      'jpeg': '🖼️',
      'gif': '🖼️',
      'pdf': '📕',
      'zip': '🗜️',
      'tar': '🗜️',
      'gz': '🗜️'
    };
    return iconMap[extension] || '📄';
  };

  // Method to update file operation status (can be called from parent component)
  const updateFileOperationStatus = (filePath, status) => {
    setFileOperationStatus(prev => ({
      ...prev,
      [filePath]: status
    }));
    
    // Clear status after 3 seconds
    setTimeout(() => {
      setFileOperationStatus(prev => {
        const newStatus = { ...prev };
        delete newStatus[filePath];
        return newStatus;
      });
    }, 3000);
  };

  // Expose the update method through a ref or callback
  React.useImperativeHandle(onFileSelect?.ref, () => ({
    updateFileOperationStatus
  }));

  if (loading) return (
    <div className="d-flex align-items-center p-3">
      <div className="spinner-border spinner-border-sm me-2" role="status"></div>
      <span>Loading files...</span>
    </div>
  );
  
  if (error) return (
    <div className="alert alert-danger m-2" role="alert">
      <small>{error}</small>
    </div>
  );

  return (
    <div className="file-tree" style={{ fontSize: '14px' }}>
      {files.length === 0 ? (
        <div className="text-muted p-3">
          <small>No files found</small>
        </div>
      ) : (
        files.map(node => renderFileNode(node, 0))
      )}
    </div>
  );
};

export default FileTree;

