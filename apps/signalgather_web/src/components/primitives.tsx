import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from 'react'

export function cx(...parts: (string | false | null | undefined)[]): string {
  return parts.filter(Boolean).join(' ')
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  busy?: boolean
}

const VARIANTS: Record<NonNullable<ButtonProps['variant']>, string> = {
  primary: 'bg-accent text-accent-ink hover:opacity-90',
  secondary: 'bg-surface-raised text-ink border border-line hover:border-ink-faint',
  danger: 'bg-transparent text-danger border border-danger/50 hover:bg-danger/10',
  ghost: 'bg-transparent text-ink-muted hover:text-ink',
}

export function Button({ variant = 'secondary', busy, className, children, ...rest }: ButtonProps) {
  return (
    <button
      {...rest}
      aria-busy={busy || undefined}
      disabled={rest.disabled || busy}
      className={cx(
        'inline-flex items-center justify-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium',
        'transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent',
        'disabled:cursor-not-allowed disabled:opacity-50',
        VARIANTS[variant],
        className,
      )}
    >
      {busy && <Spinner />}
      {children}
    </button>
  )
}

export function Spinner({ className }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cx(
        'inline-block size-3.5 shrink-0 animate-spin rounded-full border-2 border-current border-t-transparent',
        className,
      )}
    />
  )
}

export function Card({ className, children, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      {...rest}
      className={cx('rounded-xl border border-line bg-surface-raised', className)}
    >
      {children}
    </div>
  )
}

export function SectionHeading({ children, aside }: { children: ReactNode; aside?: ReactNode }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-4 py-3">
      <h2 className="text-sm font-semibold tracking-wide text-ink uppercase">{children}</h2>
      {aside}
    </div>
  )
}

/** Placeholder shown while an artifact has not been produced yet. */
export function Skeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="space-y-2.5" aria-hidden="true">
      {Array.from({ length: lines }, (_, i) => (
        <div
          key={i}
          className="h-3 animate-pulse rounded bg-line"
          style={{ width: `${90 - i * 12}%` }}
        />
      ))}
    </div>
  )
}

export function ErrorNote({ children, onRetry }: { children: ReactNode; onRetry?: () => void }) {
  return (
    <div
      role="alert"
      className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-danger/40 bg-danger/10 px-3.5 py-2.5 text-sm text-ink"
    >
      <span>{children}</span>
      {onRetry && (
        <Button variant="ghost" onClick={onRetry} className="text-danger">
          Retry
        </Button>
      )}
    </div>
  )
}

export function EmptyState({
  title,
  children,
  action,
}: {
  title: string
  children?: ReactNode
  action?: ReactNode
}) {
  return (
    <div className="rounded-xl border border-dashed border-line px-6 py-12 text-center">
      <p className="text-base font-medium text-ink">{title}</p>
      {children && <p className="mx-auto mt-2 max-w-md text-sm text-ink-muted">{children}</p>}
      {action && <div className="mt-5 flex justify-center">{action}</div>}
    </div>
  )
}
