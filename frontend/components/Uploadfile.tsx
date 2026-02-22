import { useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
type uploadstatus = "idle" | "uploading" | "success" | "error";
type Props={
  setpdf:(file:File|null)=>void;
  viewsetpdf:()=>void;
};
export default function Uploadfile({ setpdf, viewsetpdf }: Props) {
  const navigate=useNavigate();
  const [file, viewfile] = useState<File | null>(null);
  const [status, uploadfile] = useState<uploadstatus>("idle");
  const [progress, checkprogress] = useState(0);
  const [jobId, setJobId] = useState<string | null>(null);
  const [back_status,setstatus]=useState<string | null>(null)
  function getfile(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      viewfile(e.target.files[0]);
      const pdf_file=e.target.files[0];
      setpdf(pdf_file);
      uploadfile("idle");
      checkprogress(0);
    }
  }
  async function handleuploading() {
    if (!file) return;
    uploadfile("uploading");
    checkprogress(0);
    try{
      let currentProgress = 0;
      const interval = setInterval(() => {
        currentProgress += 10;
        checkprogress(currentProgress);
        if (currentProgress >= 95) {
          clearInterval(interval);
        }
      }, 300);
      console.log("sending request...");
      const formdata=new FormData();
      formdata.append("file",file);
      const res=await fetch("http://127.0.0.1:8000/upload",{
        method:"POST",
        body:formdata
      })
      if(!res.ok){
        uploadfile("error");
        checkprogress(0);
        throw new Error("Upload file failed");
      }
      const data=await res.json();
      setJobId(data.job_id);
      const id=data.job_id;
      console.log(id);
      localStorage.setItem("bookId", id);
      navigate("/pdfview", { state: { bookId: id } });
      setstatus(data.status);
      console.log("response received", data);
      uploadfile("success");
      checkprogress(100);
    }catch(err){
      console.log(err);
      uploadfile("error");
    }
  }  
  function resetUpload() {
    viewfile(null);
    setpdf(null);
    uploadfile("idle");
    checkprogress(0);
    setJobId(null);
    setstatus(null);
  }
  return (
    <div className="upload-box">
      <h1>Upload your file</h1>
      <p>Select a file to upload for further processing.</p>

      <input type="file" onChange={getfile} />

      {file && (
        <div className="file-info">
          <p>name : {file.name}</p>
          <p>size : {(file.size / 1024).toFixed(2)} KB</p>
          <p>type : {file.type}</p>
        </div>
      )}

      {status === "uploading" && (
        <div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          <p>{progress}% uploaded</p>
        </div>
      )}

      {file && status !== "uploading" && status !== "success" && status!=="error" &&(
        <button className="upload-btn" onClick={handleuploading}>
          Upload file
        </button>
      )}
      {status === "success" && (
        <div>
          <p className="success-text">File uploaded successfully!</p>

          <button className="reset-btn" onClick={resetUpload}>
            Upload another file
          </button>
          <button className="view-btn" onClick={viewsetpdf}>View Pdf</button>
        </div>
      )}

      {status === "error" && (
        <><p className="error-text">Upload failed. Please try again.</p><button className="reset-btn" onClick={resetUpload}>
          Upload another file
        </button></>
      )}
    </div>
  );
}