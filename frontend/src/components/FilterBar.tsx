import React from 'react';
import { Filter, RotateCcw, Calendar, Tag, MapPin, Truck, ShoppingBag, ShieldCheck } from 'lucide-react';
import { FilterState, FilterOptions } from '../types';

interface FilterBarProps {
  filters: FilterState;
  filterOptions: FilterOptions | null;
  onFilterChange: (key: keyof FilterState, value: string) => void;
  onResetFilters: () => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  filters,
  filterOptions,
  onFilterChange,
  onResetFilters,
}) => {
  // Count active filters
  const activeCount = Object.entries(filters).filter(([k, v]) => {
    if (k === 'startDate' || k === 'endDate') return v !== '';
    return v !== 'ALL' && v !== '';
  }).length;

  return (
    <div className="glass-card" style={{ padding: '16px 20px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={16} color="var(--accent-primary)" />
          <h2 style={{ fontSize: '0.95rem', fontWeight: 700 }}>Global Analytics Filters</h2>
          {activeCount > 0 && (
            <span className="badge badge-indigo">
              {activeCount} Active Filter{activeCount > 1 ? 's' : ''}
            </span>
          )}
        </div>

        {activeCount > 0 && (
          <button
            onClick={onResetFilters}
            className="btn-secondary"
            style={{ fontSize: '0.78rem', padding: '5px 10px', color: '#fb7185', borderColor: 'rgba(244, 63, 94, 0.25)' }}
          >
            <RotateCcw size={13} />
            <span>Reset All Filters</span>
          </button>
        )}
      </div>

      {/* Filter Select Controls Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
          gap: '12px',
        }}
      >
        {/* Category */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <Tag size={12} /> Category
          </label>
          <select
            value={filters.category}
            onChange={(e) => onFilterChange('category', e.target.value)}
            style={{ width: '100%' }}
          >
            {filterOptions?.categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat === 'ALL' ? 'All Categories' : cat}
              </option>
            )) || <option value="ALL">All Categories</option>}
          </select>
        </div>

        {/* State */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <MapPin size={12} /> Shipping State
          </label>
          <select
            value={filters.state}
            onChange={(e) => onFilterChange('state', e.target.value)}
            style={{ width: '100%' }}
          >
            {filterOptions?.states.map((st) => (
              <option key={st} value={st}>
                {st === 'ALL' ? 'All States' : st}
              </option>
            )) || <option value="ALL">All States</option>}
          </select>
        </div>

        {/* Status */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <ShieldCheck size={12} /> Order Status
          </label>
          <select
            value={filters.status}
            onChange={(e) => onFilterChange('status', e.target.value)}
            style={{ width: '100%' }}
          >
            {filterOptions?.statuses.map((stat) => (
              <option key={stat} value={stat}>
                {stat === 'ALL' ? 'All Statuses' : stat}
              </option>
            )) || <option value="ALL">All Statuses</option>}
          </select>
        </div>

        {/* Fulfilment */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <Truck size={12} /> Fulfilment Channel
          </label>
          <select
            value={filters.fulfilment}
            onChange={(e) => onFilterChange('fulfilment', e.target.value)}
            style={{ width: '100%' }}
          >
            {filterOptions?.fulfilment_types.map((f) => (
              <option key={f} value={f}>
                {f === 'ALL' ? 'All Fulfilment' : f}
              </option>
            )) || <option value="ALL">All Fulfilment</option>}
          </select>
        </div>

        {/* Sales Channel */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <ShoppingBag size={12} /> Sales Channel
          </label>
          <select
            value={filters.salesChannel}
            onChange={(e) => onFilterChange('salesChannel', e.target.value)}
            style={{ width: '100%' }}
          >
            {filterOptions?.sales_channels.map((sc) => (
              <option key={sc} value={sc}>
                {sc === 'ALL' ? 'All Channels' : sc}
              </option>
            )) || <option value="ALL">All Channels</option>}
          </select>
        </div>

        {/* Start Date */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <Calendar size={12} /> From Date
          </label>
          <input
            type="date"
            value={filters.startDate}
            min={filterOptions?.date_range.min_date}
            max={filterOptions?.date_range.max_date}
            onChange={(e) => onFilterChange('startDate', e.target.value)}
            style={{ width: '100%' }}
          />
        </div>

        {/* End Date */}
        <div>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '5px', fontWeight: 600 }}>
            <Calendar size={12} /> To Date
          </label>
          <input
            type="date"
            value={filters.endDate}
            min={filterOptions?.date_range.min_date}
            max={filterOptions?.date_range.max_date}
            onChange={(e) => onFilterChange('endDate', e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
      </div>
    </div>
  );
};
