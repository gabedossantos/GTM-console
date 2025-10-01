import { createContext, ReactNode, useContext } from 'react';

export type DesignVariant = 'design1' | 'design2';

const DesignVariantContext = createContext<DesignVariant>('design1');

interface DesignProviderProps {
  variant: DesignVariant;
  children: ReactNode;
}

export function DesignProvider({ variant, children }: DesignProviderProps) {
  return <DesignVariantContext.Provider value={variant}>{children}</DesignVariantContext.Provider>;
}

export function useDesignVariant(): DesignVariant {
  return useContext(DesignVariantContext);
}
