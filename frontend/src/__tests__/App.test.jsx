import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders PriceVision title', () => {
    render(<App />);
    expect(screen.getByText(/Price/i)).toBeInTheDocument();
    expect(screen.getByText(/Vision/i)).toBeInTheDocument();
  });
});
