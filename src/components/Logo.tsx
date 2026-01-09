import Image from 'next/image';
import Link from 'next/link';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  showLink?: boolean;
}

export default function Logo({ size = 'md', className = '', showLink = true }: LogoProps) {
  const dimensions = {
    sm: { width: 150, height: 60 },
    md: { width: 200, height: 80 },
    lg: { width: 250, height: 100 }
  };

  const LogoImage = (
    <Image
      src="/logo-transparent.png"
      alt="domulex.ai - Rechtliche KI-Plattform"
      width={dimensions[size].width}
      height={dimensions[size].height}
      className={`object-contain ${className}`}
      priority
    />
  );

  if (showLink) {
    return (
      <Link href="/" className="flex items-center">
        {LogoImage}
      </Link>
    );
  }

  return LogoImage;
}
