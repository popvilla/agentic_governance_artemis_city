import Link from 'next/link';

const CustomLink = (props) => {
  const href = props.href;
  const isInternalLink = href && (href.startsWith('/') || href.startsWith('#'));

  if (isInternalLink) {
    return (
      <Link href={href} {...props}>
        {props.children}
      </Link>
    );
  }

  return <a target="_blank" rel="noopener noreferrer" {...props} />;
};

const components = {
  a: CustomLink,
  // Example: Custom Heading (You can style it with Tailwind)
  h1: (props) => <h1 className="text-4xl font-extrabold text-blue-800 mt-10 mb-4" {...props} />,
  h2: (props) => <h2 className="text-3xl font-bold text-blue-700 mt-8 mb-3 border-b pb-2" {...props} />,
  p: (props) => <p className="text-lg leading-relaxed mb-6" {...props} />,
  ul: (props) => <ul className="list-disc list-inside mb-6 pl-5" {...props} />,
  li: (props) => <li className="mb-2" {...props} />,
  // You can add more custom components here, e.g.:
  // MyCustomComponent: (props) => <div className="bg-yellow-100 p-4 rounded" {...props} />,
};

export default components;
