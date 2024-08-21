import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Examples Substrate NextJS app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css" />
      </head>
      <body>{children}</body>
    </html>
  );
}
