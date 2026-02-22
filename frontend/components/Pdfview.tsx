import { useEffect, useState } from "react";
import { Document, Page } from "react-pdf";
import { useLocation } from "react-router-dom";
import {TransformWrapper,TransformComponent} from "react-zoom-pan-pinch";
type Props = {
  pdfFile: File | null;
};
export default function Pdfview({ pdfFile }: Props) {
  const location = useLocation();
  const bookId =location.state?.bookId || localStorage.getItem("bookId");
  console.log(bookId);
  const [numPages, setNumPages] = useState<number>();
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [pdf_type,setpdf_type] = useState<string|null>(null);
  const [page_no,setpage_no] = useState<any[]>([]);
  const [loaddata,setloaddata]=useState(false);
  const [im_url,setim_url]=useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
  }
  useEffect(()=>{
    if(!bookId) return;
    const get_info=async () => {
      try{
        setloaddata(true);
        const res_info=await fetch(`http://127.0.0.1:8000/get_pro/${bookId}`);
        if(!res_info.ok){
          throw new Error("not found failed");
        }
        const data_info=await res_info.json();
        setpdf_type(data_info.pdf_type);
        setpage_no(data_info.pages);
        console.log(data_info.pdf_type);
      }catch(err){
        console.error("Error fetching processed data:", err);
      }
      finally {
        setloaddata(false);
      }
    }
    get_info();
  },[bookId])
  console.log("PAGENO",page_no)
  const firstpage=page_no.length>0?page_no[0].pageno:null;
  const con=pdf_type==="text_type"&&firstpage!=null&&pageNumber >= firstpage;
  console.log("CON : ",con)
  const handle_generate = async (currentPageNumber: number) => {
  console.log("CU1 : ",currentPageNumber);
  const currentPageObj = page_no.find(p => p.pageno === currentPageNumber);
  console.log("CU2 : ",currentPageObj);
  if (!currentPageObj) {
    console.error("Page object not found");
    return;
  }

  try {
    setIsGenerating(true);
    setim_url(null);
    const response = await fetch("http://127.0.0.1:8000/generate_image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(currentPageObj), // send only the single page object
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    console.log("Image generation response:", data);
    setim_url(data);
  } catch (err) {
    console.error(err);
  }finally{
    setIsGenerating(false);
  }
};
  if (!pdfFile) {
    return <p>No PDF selected</p>;
  }

  return (
    <div className="page-div">
      <div className="book">
      <div className="page">
<TransformWrapper
  initialScale={1}
  minScale={1}
  maxScale={1.5}
  wheel={{ step: 0.1 }}
  doubleClick={{ disabled: true }}
>
  {({ zoomIn, zoomOut }) => (
    <>
      {/* Controls */}
      <div className="upper" style={{ marginBottom: "8px" }}>
        <button onClick={() => zoomIn()}>Zoom In</button>
        <button onClick={() => zoomOut()}>Zoom Out</button>
        <button onClick={() =>  setloaddata(false)}>Reset</button>
      </div>

      {/* Zoomable PDF */}
      <TransformComponent>
        <Document file={pdfFile} onLoadSuccess={onDocumentLoadSuccess}>
          <Page
            pageNumber={pageNumber}
            renderAnnotationLayer={false}
            renderTextLayer={false}
          />
        </Document>
      </TransformComponent>
    </>
  )}
</TransformWrapper>
      </div>
     <div className="right">
      {isGenerating ? (
        <div className="wait-box">
        <div className="spinner" />
        <p>Generating image…</p>
        <p className="sub">This may take a few seconds</p>
      </div>
        ):im_url ? (
        <img
        src={im_url}
        alt="Generated"
        style={{
        maxWidth: "100%",
        maxHeight: "150vh",
        borderRadius: "8px"
        }}
        className="img"
        />
        ):loaddata ? (
          <p>Checking document type...</p>
        ) : pdf_type !== "text_type" ? (
          <p>Scanned PDF cannot generate images.</p>
        ) : (
          <button className="get_image_button"
            disabled={!con}
            onClick={() => handle_generate(pageNumber)}
          >
            {firstpage && pageNumber < firstpage
              ? `Available from page ${firstpage}`
              : "Generate Image"}
          </button>
        )}         
      </div>
      </div>
      <div className="tool-control">
      <p>
        Page {pageNumber} of {numPages}
      </p>

      <button
        disabled={pageNumber <= 1}
        onClick={() => setPageNumber(pageNumber - 1)}
      >
        Prev
      </button>

      <button
        disabled={numPages === undefined || pageNumber >= numPages}
        onClick={() => setPageNumber(pageNumber + 1)}
      >
        Next
      </button>
      
      </div>
    </div>
  );
}
