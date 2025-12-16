import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className="hero">
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className="hero__actions">
          <Link
            className="button button--primary button--lg"
            to="/docs/introduction">
            Get Started
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/chatbot">
            Book Assistant
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({title, description, icon}) {
  return (
    <div className="card">
      <div className="card__body text--center padding-horiz--md">
        <div className="feature-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className="padding-vert--lg">
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <FeatureCard
              title="Comprehensive Coverage"
              description="Complete textbook covering all aspects of Physical AI and Humanoid Robotics."
              icon="🤖"
            />
          </div>
          <div className="col col--4">
            <FeatureCard
              title="Interactive Learning"
              description="Integrated chatbot for real-time questions and answers about the content."
              icon="💬"
            />
          </div>
          <div className="col col--4">
            <FeatureCard
              title="Open Source"
              description="Freely available educational resource for students and researchers."
              icon="📖"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An Open Educational Resource for Advanced Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <section className="padding-vert--lg">
          <div className="container text--center">
            <h2>Ready to dive into Physical AI & Humanoid Robotics?</h2>
            <p className="padding-horiz--md">
              Explore our comprehensive textbook covering the fundamentals and advanced concepts of Physical AI and Humanoid Robotics.
            </p>
            <div className="padding-vert--md">
              <Link
                className="button button--primary button--lg margin-horiz--sm"
                to="/docs/introduction">
                Textbook
              </Link>
              <Link
                className="button button--secondary button--lg margin-horiz--sm"
                to="/chatbot">
                Chatbot
              </Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}