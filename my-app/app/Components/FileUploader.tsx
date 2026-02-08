"use client";

// TODO: UPLOAD PROGRESS BAR
import { ChangeEvent, useState } from "react";
import axios from "axios";
export default function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  type fileStatus = "idle" | "uploading" | "success" | "error";
  const [status, Setstatus] = useState<fileStatus>("idle");
  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      setFile(e.target.files[0]);
      const allowedTypes = [
        "video/mp4",
        "audio/mpeg",
        "video/mov",
        "video/avi",
        "audio/wav",
        "audio/m4a",
        "video/webm",
        "audio/opus",
      ];
      if (!allowedTypes.includes(e.target.files[0].type)) {
        alert("Invalid file type");
        setFile(null);
        return;
      }
    }
  }
  async function uploadFile() {
    if (!file) return;
    Setstatus("uploading");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/uploadFile",
        formData,
      );
      if (response.data.success) {
        Setstatus("success");
        alert("File Uploaded Successfully");
      } else {
        Setstatus("error");
        alert("Upload Failed");
      }
    } catch (error) {
      Setstatus("error");
    }
  }
  return (
    <div className="space-y-2">
      <input
        type="file"
        accept=".mp4, .mp3, .mov, .avi, .wav, .m4a, .webm, .opus, .mpeg "
        onChange={handleFileChange}
      />
      {file && (
        <div className="mb-4 text-sm">
          <p>File name: {file.name}</p>
          <p>Size: {(file.size / 1024).toFixed(2)}</p>
          <p>Type: {file.type}</p>
        </div>
      )}
      {file && status !== "uploading" && (
        <button onClick={uploadFile}>Upload</button>
      )}
      {status === "success" && (
        <p className="text-sm text-green-600">File Uploaded !</p>
      )}
      {status === "error" && (
        <p className="text-sm text-red-600">Upload Failed</p>
      )}
    </div>
  );
}
