import { useState } from "react";
import Uploadfile from "./components/Uploadfile";
import Pdfview from "./components/Pdfview";

import { pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

function App() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [showPdf, setShowPdf] = useState(false);
  

  return (
    <div>
      {!showPdf ? (
        <Uploadfile
          setpdf={setPdfFile}
          viewsetpdf={() => setShowPdf(true)}
        />
      ) : (
        <div>
          <Pdfview pdfFile={pdfFile} />
        </div>
      )}
    </div>
  );
}

export default App;
