import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import DocsFile from "./markdown/documentation.md";
import rehypeSlug from "rehype-slug";

export const Documentation = (): JSX.Element => {
  const [markdown, setMarkdown] = useState("");

  useEffect(() => {
    fetch(DocsFile)
      .then((response) => response.text())
      .then((text) => setMarkdown(text));
  }, []);

  return (
    <div>
      <ReactMarkdown rehypePlugins={[rehypeSlug]} children={markdown} />
    </div>
  );
};

export default Documentation;
