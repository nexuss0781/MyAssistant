
import React from 'react';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import FileTree from './FileTree';
import ChatLog from './ChatLog';

const VSCodeLayout = () => {
  return (
    <PanelGroup direction="horizontal">
      <Panel defaultSize={20}>
        <FileTree />
      </Panel>
      <PanelResizeHandle />
      <Panel>
        <PanelGroup direction="vertical">
          <Panel>
            {/* This will be the Code Editor */}
            <div style={{ padding: '1rem' }}>
              <h2>Code Editor</h2>
            </div>
          </Panel>
          <PanelResizeHandle />
          <Panel defaultSize={30}>
            <ChatLog />
          </Panel>
        </PanelGroup>
      </Panel>
    </PanelGroup>
  );
};

export default VSCodeLayout;
