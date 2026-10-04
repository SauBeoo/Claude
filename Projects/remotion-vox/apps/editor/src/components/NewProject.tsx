// NewProject.tsx — wizard with the 3 auto-edit entry points:
//   ① import pipeline video (stem + channel)
//   ② auto collage (audio + srt [+ plan])
//   ③ caption-only (video + srt)
// Each spawns a python job on the server; on success the project list refreshes.

import React, {useState} from 'react';
import {getJob, runImport} from '../api';

type Mode = 'pipeline' | 'collage' | 'captions' | 'vlog';

// Định nghĩa NGOÀI component — khai báo trong render sẽ đổi identity mỗi
// keystroke khiến React remount input và mất focus (bug bắt được 2026-08-16).
const F: React.FC<{label: string; v: string; set: (s: string) => void; ph?: string}> = ({
  label, v, set, ph,
}) => (
  <label className="insp-field">
    <span>{label}</span>
    <input value={v} placeholder={ph} onChange={(e) => set(e.target.value)} />
  </label>
);

export const NewProject: React.FC<{
  onClose: () => void;
  onCreated: (name: string) => void;
}> = ({onClose, onCreated}) => {
  const [mode, setMode] = useState<Mode>('pipeline');
  const [out, setOut] = useState('');
  const [stem, setStem] = useState('');
  const [channel, setChannel] = useState('health');
  const [audio, setAudio] = useState('');
  const [srt, setSrt] = useState('');
  const [plan, setPlan] = useState('');
  const [video, setVideo] = useState('');
  const [clipsDir, setClipsDir] = useState('');
  const [title, setTitle] = useState('VLOG');
  const [seconds, setSeconds] = useState('15');
  const [size, setSize] = useState('1080x1920');
  const [status, setStatus] = useState('');

  const run = async () => {
    if (!out) return setStatus('🔴 cần tên project (--out)');
    let tool = '';
    let args: string[] = [];
    if (mode === 'pipeline') {
      if (!stem) return setStatus('🔴 cần stem');
      tool = 'import_pipeline.py';
      args = ['--stem', stem, '--channel', channel, '--out', out];
    } else if (mode === 'collage') {
      if (!audio) return setStatus('🔴 cần đường dẫn audio');
      tool = 'auto_collage.py';
      args = ['--audio', audio, '--out', out];
      if (srt) args.push('--srt', srt);
      if (plan) args.push('--plan', plan);
    } else if (mode === 'vlog') {
      if (!clipsDir) return setStatus('🔴 cần folder chứa clip');
      tool = 'auto_vlog.py';
      args = ['--clips', clipsDir, '--out', out, '--title', title,
        '--seconds', seconds, '--size', size];
      if (audio) args.push('--music', audio);
    } else {
      if (!video || !srt) return setStatus('🔴 cần video + srt');
      tool = 'import_caption_job.py';
      args = ['--video', video, '--srt', srt, '--out', out];
    }
    setStatus('⏳ đang chạy…');
    try {
      const {jobId} = await runImport(tool, args);
      const poll = async (): Promise<void> => {
        const job = await getJob(jobId);
        if (!job.done) {
          setStatus(`⏳ ${job.logTail.split('\n').filter(Boolean).pop() ?? '…'}`);
          setTimeout(poll, 1500);
          return;
        }
        if (job.exitCode === 0) {
          setStatus('✅ xong');
          onCreated(out);
        } else {
          setStatus(`🔴 lỗi (exit ${job.exitCode}):\n${job.logTail.slice(-600)}`);
        }
      };
      poll();
    } catch (e) {
      setStatus(`🔴 ${String(e)}`);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>Project mới</h3>
        <div className="modal-tabs">
          <button className={mode === 'pipeline' ? 'primary' : ''} onClick={() => setMode('pipeline')}>
            Từ pipeline kênh
          </button>
          <button className={mode === 'collage' ? 'primary' : ''} onClick={() => setMode('collage')}>
            Auto collage
          </button>
          <button className={mode === 'captions' ? 'primary' : ''} onClick={() => setMode('captions')}>
            Chỉ phụ đề
          </button>
          <button className={mode === 'vlog' ? 'primary' : ''} onClick={() => setMode('vlog')}>
            VLOG beat-edit
          </button>
        </div>

        <F label="tên project" v={out} set={setOut} ph="vd: cabbage-34" />
        {mode === 'pipeline' && (
          <>
            <F label="stem" v={stem} set={setStem} ph="34_cabbage-asa-yoru" />
            <F label="channel" v={channel} set={setChannel} ph="health" />
          </>
        )}
        {mode === 'collage' && (
          <>
            <F label="audio" v={audio} set={setAudio} ph="E:\\...\\voice.mp3" />
            <F label="srt (khuyên dùng)" v={srt} set={setSrt} ph="E:\\...\\subs.srt" />
            <F label="plan.json (tuỳ chọn)" v={plan} set={setPlan} ph="scene plan có heroQuery" />
          </>
        )}
        {mode === 'captions' && (
          <>
            <F label="video" v={video} set={setVideo} ph="E:\\...\\video.mp4" />
            <F label="srt" v={srt} set={setSrt} ph="E:\\...\\subs.srt" />
          </>
        )}
        {mode === 'vlog' && (
          <>
            <F label="folder clip" v={clipsDir} set={setClipsDir} ph="E:\\...\\footage (mp4/mov)" />
            <F label="nhạc (tuỳ chọn)" v={audio} set={setAudio} ph="E:\\...\\music.mp3 — trống = synth beat" />
            <F label="title" v={title} set={setTitle} />
            <F label="giây" v={seconds} set={setSeconds} />
            <F label="khung" v={size} set={setSize} ph="1080x1920 hoặc 1920x1080" />
          </>
        )}

        <div className="modal-actions">
          <button onClick={onClose}>Đóng</button>
          <button className="primary" onClick={run}>Tạo</button>
        </div>
        <pre className="modal-status">{status}</pre>
      </div>
    </div>
  );
};
