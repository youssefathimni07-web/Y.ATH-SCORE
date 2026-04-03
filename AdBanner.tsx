import { useEffect } from "react";

export default function AdBanner() {
  useEffect(() => {
    try {
      (window as any).adsbygoogle = (window as any).adsbygoogle || [];
      (window as any).adsbygoogle.push({});
    } catch (e) {}
  }, []);

  return (
    <ins
      className="adsbygoogle"
      style={{ display: "block" }}
      data-ad-client="ca-pub-XXXXXXXXXXXX"
      data-ad-slot="XXXXXXXX"
      data-ad-format="auto"
    />
  );
}
