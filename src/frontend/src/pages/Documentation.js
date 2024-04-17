import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import DocsFile from "./markdown/documentation.md";

export const Documentation = (): JSX.Element => {
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    fetch(DocsFile)
      .then((response) => response.text())
      .then((text) => setMarkdown(text));
  }, []);

  return (
    <div>
      <ReactMarkdown children={markdown} />
    </div>
  );
};

export default Documentation;
